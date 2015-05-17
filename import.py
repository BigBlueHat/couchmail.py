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

# IMAP setup
host = config.get('imap', 'host')
user = config.get('imap', 'user')
try:
    password = config.get('imap', 'password')
except ConfigParser.NoOptionError:
    password = getpass.getpass("Password for %s on %s: " % (user, host))
mailbox = config.get('imap', 'mailbox')

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
                archive_msg(couch, msg)
        except ResourceNotFound:
            # add the msg to the archive
            archive_msg(couch, msg)
