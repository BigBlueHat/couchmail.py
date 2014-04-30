# -*- coding: utf-8 -*-

"""
couchmail
~~~~~~~~

IMAP => Apache CouchDB (and Cloudant) archiver/importer/thing

:license: Apache License 2.0, see LICENSE for more details.
"""

__title__ = 'couchmail'

from .couchmail import archive_msg, headers, truly_unique_id

__all__ = ['archive_msg', 'headers', 'truly_unique_id']
