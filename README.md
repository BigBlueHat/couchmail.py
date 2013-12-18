# couchmail.py

**Very** early stage email archiver for Apache CouchDB
and Cloudant.

## Installation

Copy `config.sample.ini` to `config.ini`.
Customize it.

    $ pip install easyimap couchdb
    $ python couchmail.py

Hope for the best!

It *should* export the number of emails you specify,
store them by their `Message-ID` header value (or
timestamp...if `Message-ID` is missing).

## Included Design Doc

There are some very rudamentary MapReduce Views
included.

    $ cd couchapp
    $ couchapp push . http://user:pass@localhost:5984/mail

`erica` (the future of `couchapp`) should also work.

## License

Apache License 2.0
