
"""CouchMail.py imports your mail from an IMAP server into a CouchDB database

License: Apache 2.0 - http://opensource.org/licenses/Apache-2.0
"""

import calendar
from base64 import b64encode

from dateutil.parser import parse
from couchdb import ResourceConflict

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

def truly_unique_id(msg):
    # TODO: check `date` header existence?
    if msg.message_id:
        unique_id = msg.message_id.strip()
    else:
        dt = parse(msg.date)
        unique_id = calendar.timegm(dt.timetuple())
    return unique_id

def archive_msg(couch, msg):
    dt = parse(msg.date)
    hdrs = headers(msg)
    doc_id = truly_unique_id(msg)

    base_doc = {'_id': doc_id,
           'headers': hdrs,
           'date': [dt.year, dt.month, dt.day, dt.hour, dt.minute,
               dt.second],
           'to': msg.to,
           'from': msg.from_addr,
           'sender': msg.sender,
           'cc': msg.cc,
           'deliveredto': msg.delivered_to,
           'references': msg.references,
           'subject': msg.title,
           'message': msg.body}

    # clean out empty values top-level keys
    doc = dict((k,v) for k, v in base_doc.iteritems() if v)

    # Add the raw message content for "auditing"
    doc['_attachments'] = parts(msg.attachments)
    doc['_attachments']['raw.eml'] = {
            'content_type': 'message/rfc822',
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
