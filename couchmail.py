#!/usr/bin/env python

"""CouchMail.py imports your mail from an IMAP server into a CouchDB database

License: Apache 2.0 - http://opensource.org/licenses/Apache-2.0
"""

import calendar
import ConfigParser
from datetime import datetime
import os
import email
import mimetypes
import getpass
from base64 import b64encode

import easyimap
from dateutil.parser import parse
from couchdb import Server, ResourceConflict, ResourceNotFound

config = ConfigParser.RawConfigParser()
config.read('config.ini')

# CouchDB/Cloudant setup
server = Server(config.get('couch', 'server'))
couch = server[config.get('couch', 'db')]

# IMAP setup
host = config.get('imap', 'host')
user = config.get('imap', 'user')
try:
    password = config.get('imap', 'password')
except ConfigParser.NoOptionError:
    password = getpass.getpass("Password for %s on %s: " % (user, host))
mailbox = config.get('imap', 'mailbox')

def headers(msg):
    mail = {}
    for header, value in msg._message.items():
        header = header.lower()
        if header in mail:
            if isinstance(mail[header], str):
                mail[header] = [mail[header], value]
            else:
                mail[header].append(value)
        else:
            mail[header] = value
    return mail

def parts(attachments):
    parts = {}
    for (filename, data, content_type) in attachments:
        parts[filename] = {'content_type': content_type,
                'data': b64encode(data)}
    return parts

def truly_unique_id(headers):
    if 'message-id' in headers:
        unique_id = headers['message-id']
    else:
        unique_id = calendar.timegm(dt.timetuple())
    return unique_id

def archive_msg(msg):
    dt = parse(msg.date)
    hdrs = headers(msg)
    doc_id = truly_unique_id(hdrs)

    base_doc = {'_id': doc_id,
           'headers': hdrs,
           'date': [dt.year, dt.month, dt.day, dt.hour, dt.minute,
               dt.second],
           'to': msg.to,
           'from': msg.from_addr,
           'sender': msg.sender,
           'cc': msg.cc,
           'deliveredto': msg.deliveredto,
           'references': msg.references,
           'subject': msg.title,
           'message': msg.body}

    # clean out empty values top-level keys
    doc = dict((k,v) for k, v in base_doc.iteritems() if v)

    # Add the raw message content for "auditing"
    doc['_attachments'] = parts(msg.attachments)
    doc['_attachments']['raw.eml'] = {
            'content_type': msg.contenttype[:msg.contenttype.find(';')] \
                    if msg.contenttype else 'text/plain',
            'data': b64encode(msg.raw)}

    if doc_id in couch:
        doc['_rev'] = couch[doc_id]['_rev']

    try:
        couch.save(doc)
        if '_rev' in doc:
            print doc_id + ' updated.'
        else:
            print doc_id + ' stored.'
    except ResourceConflict:
        print doc_id + ' could not be updated.'

if __name__ == '__main__':
    print 'Connecting...'
    imapper = easyimap.connect(host, user, password, mailbox, read_only=True)
    print 'Connected. Couple more questions...'
    amount = int(raw_input('How many mail items would you like to archive? '))
    should_skip = raw_input('Skip mail already archived (y/n)? ')
    if should_skip.lower() in ["y", "yes", "yea", "si", "go", "aye", "sure"]:
      should_skip = True
    else:
      should_skip = False
    # Loop through the messages and add them to CouchDB
    ids = imapper.listids(amount)
    for id in ids:
        msg = imapper.mail(id, include_raw=True)
        unique_id = truly_unique_id(headers(msg))
        try:
            current_doc = couch[unique_id]
            if should_skip:
                print 'Skipping ' + unique_id + ' (already archived)'
                continue
            else:
                # archive document exists, but user wants to overwrite it
                archive_msg(msg)
        except ResourceNotFound:
            # add the msg to the archive
            archive_msg(msg)
