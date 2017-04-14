Requests-FTP
============

Requests-FTP is an implementation of a very stupid FTP transport adapter for
use with the awesome `Requests`_ Python library.

This library is *not* intended to be an example of Transport Adapters best
practices. This library was cowboyed together in about 4 hours of total work,
has no tests, and relies on a few ugly hacks. Instead, it is intended as both
a starting point for future development and a useful example for how to
implement transport adapters.

Here's how you use it:

.. code-block:: pycon

    >>> import requests
    >>> import requests_ftp
    >>> requests_ftp.monkeypatch_session()
    >>> s = requests.Session()
    >>> resp = s.list('ftp://127.0.0.1/', auth=('Lukasa', 'notmypass'))
    >>> resp.status_code
    '226'
    >>> print resp.content
    ...snip...
    >>> resp = s.stor('ftp://127.0.0.1/test.txt', auth=('Lukasa', 'notmypass'),
                       files={'file': open('report.txt', 'rb')})


Features
--------

Almost none!

- Adds the FTP LIST, STOR, RETR and NLST verbs via a new FTP transport adapter.
- Provides a function that monkeypatches the Requests Session object, exposing
  helper methods much like the current ``Session.get()`` and ``Session.post()``
  methods.
- Piggybacks on standard Requests idioms: uses normal Requests models and
  access methods, including the tuple form of authentication.

Does not provide:

- Connection pooling! One new connection and multiple commands for each
  request, including authentication. **Super** inefficient.
- SFTP. Security is for the weak.
- Less common commands.

Important Notes
---------------

Many corners have been cut in my rush to get this code finished. The most
obvious problem is that this code does not have *any* tests. This is my highest
priority for fixing.

More notably, we have the following important caveats:

- The design of the Requests Transport Adapater means that the STOR method
  has to un-encode a multipart form-data encoded body to get the file. This is
  painful, and I haven't tested this thoroughly, so it might not work.
- **Massive** assumptions have been made in the use of the STOR method. This
  code assumes that there will only be one file included in the files argument.
  It also requires that you provide the filename to save as as part of the URL.
  This is single-handedly the most brittle part of this adapter.
- This code is not optimised for performance AT ALL. There is some low-hanging
  fruit here: we should be able to connection pool relatively easily, and we
  can probably avoid making some of the requests we do.

Contributing
------------

Please do! I would love for this to be developed further by anyone who is
interested. Wherever possible, please provide unit tests for your work (yes,
this is very much a 'do as I say, not as I do' kind of moment). Don't forget
to add your name to AUTHORS.

License
-------

To maximise compatibility with Requests, this code is licensed under the Apache
license. See LICENSE for more details.

.. _`Requests`: https://github.com/kennethreitz/requests

