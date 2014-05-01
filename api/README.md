# UI/API (work-in-progress)

The API is built using [aspen.io](http://aspen.io/) and it's sole purpose is to provide email obfuscation. If you don't need to obfuscate email addresses (as you're hosting this locally or some such), then don't bother with the API dir (unless you want to help!). ^_^

It has also begone to grow a UI...because...

```
$ cd api/
$ pip install -r requirements.txt --allow-external Cheroot --allow-unverified Cheroot
$ # sorry about the Cheroot stuff...
$ ./serve.py
```

`http://localhost:8080/?q=fauxton` (where `fauxton` is your favorite search term) should get you some search results.

`http://localhost:8080/2013/?q=fauxton` same as above, but narrowed to 2013.

`http://localhost:8080/2013/11/?q=fauxton` same as above, but narrowed to November 2013.
