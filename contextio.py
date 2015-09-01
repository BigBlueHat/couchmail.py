#!/usr/bin/env python

"""CouchMail.py imports your mail from an IMAP server into a CouchDB database

License: Apache 2.0 - http://opensource.org/licenses/Apache-2.0
"""

import argparse
import calendar
import ConfigParser
from datetime import datetime
import os
import email
import mimetypes
import getpass
from base64 import b64encode
import json

import requests
from requests_oauthlib import OAuth1Session

import easyimap
from dateutil.parser import parse
from couchdb import Server, ResourceConflict, ResourceNotFound
from couchmail import archive_msg, headers, truly_unique_id

argparser = argparse.ArgumentParser()
argparser.add_argument('config_file', type=file,
        help="Config INI file. See `config.sample.ini` for info.")
args = argparser.parse_args()

config = ConfigParser.RawConfigParser()
config.readfp(args.config_file)

# CouchDB/Cloudant setup
server = Server(config.get('couch', 'server'))
try:
    couch = server[config.get('couch', 'db')]
except ResourceNotFound:
    couch = server.create(config.get('couch', 'db'))

# context.io setup
KEY = config.get('context.io', 'key')
SECRET = config.get('context.io', 'secret')
address = config.get('context.io', 'address')

# 2.0 API endpoint
api_url = "https://api.context.io/2.0/"

def newest_archived():
    results = couch.view('couchmail/by_timestamp', None,
                         limit=1, reduce=False, descending=True)
    for row in results:
        return row['key']

def oldest_archived():
    results = couch.view('couchmail/by_timestamp', None,
                         limit=1, reduce=False)
    for row in results:
        return row['key']

def message_to_doc(message):
    doc = message
    msg_type = doc['headers']['Content-Type'][0]
    msg_type_split = msg_type[:msg_type.find(';')]
    doc['_id'] = doc['email_message_id']
    doc['_attachments'] = {}
    doc['_attachments']['raw.eml'] = {
        'content_type': msg_type_split,
        'data': b64encode(doc['source'])
    }
    return doc


if __name__ == '__main__':
    print 'Connecting...'
    contextio = OAuth1Session(KEY, SECRET)
    # get the account info
    r = contextio.get(api_url + 'accounts',
            params={'email': address})
    account = r.json()[0]

    # rashly assume all is well...
    print 'Connected. Couple more questions...'
    amount = int(raw_input('How many mail items would you like to archive? '))
    should_skip = raw_input('Skip mail already archived (y/n)? ')
    if should_skip.lower() in ["y", "yes", "yea", "si", "go", "aye", "sure"]:
      should_skip = True
    else:
      should_skip = False
    # Loop through the messages and add them to CouchDB

    # get the most recent messages for the account
    messages = contextio.get(account['resource_url'] + '/messages',
        params={'include_body': 1, 'include_headers': 1,'include_source': 1,
            'limit': amount, 'date_before': oldest_archived()})
    for msg in messages.json():
        msg_id = msg['email_message_id']
        try:
            # check to see if doc exists
            current_doc = couch[msg_id]
            if should_skip:
                print 'Skipping ' + msg_id + ' (already archived)'
                continue
            else:
                # archive document exists, but user wants to overwrite it
                # so get the full message from context.io
                message = contextio.get(account['resource_url'] + '/messages/'
                    + msg_id,
                    params={'include_body': 1, 'include_headers': 1,
                        'include_source': 1}).json()

                doc = message_to_doc(message)
                doc['_rev'] = current_doc['_rev']

                doc_id, doc_rev = couch.save(doc)
                print 'Updated ' + doc_id
        except ResourceNotFound:
            message = contextio.get(account['resource_url'] + '/messages/'
                + msg_id,
                params={'include_body': 1, 'include_headers': 1,
                    'include_source': 1}).json()

            doc = message_to_doc(message)
            # add the msg to the archive
            doc_id, doc_rev = couch.save(doc)
            print 'Added ' + doc_id

