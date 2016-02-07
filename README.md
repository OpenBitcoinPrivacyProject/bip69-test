# bip69-test

Tests whether transactions are BIP-69 compliant.

BIP-69 is a standard for formatting Bitcoin transactions to preserve security and privacy.

https://github.com/bitcoin/bips/blob/master/bip-0069.mediawiki

## Dependencies

Tested with Python 2.7.

## Usage

From the command-line:
`python app.py 0afa520fd1d5c36d026556599de455946608a8f1908ddc02db8da5fd96a25651`

This can also be used as a CGI module on a website by sending a request with the GET parameter `txid`.

You can use the code live here:
http://www.openbitcoinprivacyproject.org/bip69-test/

## Tests

* `./run_slow_tests.sh`
* `./run_quick_tests.sh`

## Primary Authors

Kristov Atlas (email: firstname @ openbitcoinprivacyproject.org)
