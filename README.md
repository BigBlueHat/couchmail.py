# couchmail.py

**Very** early stage email archiver for Apache CouchDB
and Cloudant.

## Installation

Copy `config.sample.ini` to `config.ini`.
Customize it.

    $ pip install -r requirements.txt
    $ python import.py

Hope for the best!

It *should* export the number of emails you specify,
store them by their `Message-ID` header value (or
timestamp...if `Message-ID` is missing).

## Design Doc (aka CouchApp)

    $ cd couchapp
    $ couchapp push . http://user:pass@localhost:5984/mail

Note: `erica` should also work.

#### Full-Text Search

The Design Doc includes basic MapReduce for counting things (see Futon, Fauxton, or the Cloudant Dashboard for more).

It also includes some [Cloudant](http://cloudant.com/) specific Full-Text Search indexes. These indexes let you search email addresses, subject lines, and message bodies.

Here are some examples…

Search for "fauxton":

```
/couchdb-mailing-lists/_design/couchmail/_search/mail?q=fauxton
```

Count those results by `subject`, `to`, and `from`:

```
/couchdb-mailing-lists/_design/couchmail/_search/mail?q=fauxton&counts=["subject", "to", "from"]
```

Now drilldown those results to just what I've posted:

```
/couchdb-mailing-lists/_design/couchmail/_search/mail?q=fauxton&counts=["subject", "to", "from"]&drilldown=["from", "Benjamin Young <byoung@bigbluehat.com>"]
```

## License

[Apache License 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)
