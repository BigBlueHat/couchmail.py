#!/usr/bin/env python

"""
Copyright 2014 Benjamin Young (aka BigBlueHat)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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

import easyimap
from dateutil.parser import parse
from couchdb import Server, ResourceConflict, ResourceNotFound
from couchmail import archive_msg, headers, truly_unique_id

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
