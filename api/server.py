#!/usr/bin/env python

"""Basic UI/API to obfuscate email addresses and explain what's here
"""

from aspen.server import Server

if __name__ == '__main__':
    Server().main(['--www_root=www', '--project_root=app'])
