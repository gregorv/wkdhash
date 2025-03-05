# wkdhash

Calculate Web-Key-Directory hashes of OpenPGP UIDs.

The [Web-Key-Directory (WKD)](https://wiki.gnupg.org/WKD) is a method for
deploying OpenPGP public keys for an email address through HTTPS.

For this, the keys user IDs are decomposed into their mailbox local part
(the thing before the @ sign). This is then sha1 hashed and z-base-32 encoded,
resulting in the "hu" (hashed user-id, I guess?).

The public key is then made available under a well-known URL containing the
hu. So to deploy your public key to your webserver, you have to figure out
what your uid's hu is. This can be done with

```bash
gpg --list-keys --with-wkd-hash $IDENTITY
```

but it is not easily doable from Python when using python-gnupg.

## Command-line-utility

A simple command line utility entry-point is provided by this package,
which reads user IDs from an input stream (default stdin) and writes
the hu to an output stream (default stdout). So this module can also
be used for bash scripting.


```
usage: wkdhash [-h] [-F] [-o outfile] [infile]

Read OpenPGP User IDs line-by-line and print their corresponding Web-Key-Directory hashed-user-id (hu).

positional arguments:
  infile                Input OpenPGP UserID, defaults to stdin

options:
  -h, --help            show this help message and exit
  -F, --full            If set, output 'hu@domain', instead of just 'hu'
  -o, --output outfile  Output, default stdout

MIT License, Copyright (c) 2025 Gregor Vollmer
```

### Example Usage
```bash
$ echo "mail@example.com" | poetry run wkdhash
dizb37aqa5h4skgu7jf1xjr4q71w4paq
$ echo "Test User <mail@example.com>" | poetry run wkdhash -F
dizb37aqa5h4skgu7jf1xjr4q71w4paq@example.com
$ poetry run wkdhash
mail@example.com^Ddizb37aqa5h4skgu7jf1xjr4q71w4paq
```
