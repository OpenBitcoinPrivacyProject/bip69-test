#!/usr/bin/env python
'''Test if txid corresponds to a BIP-69 compliant tx and print relevant text.

Prints one of the following in JSON format:
    * {'compatible': 'true|false'}
    * {'error_message': 'some error message'}
'''

import string
import sys
import cgi
import http #http.py
import bip69 #bip69.py

WEB_MODE = False #flag

TX_HASH_CHAR_LEN = 64
INVALID_ERR_MSG = "Requires one paramter 'txid' as 64-character hex string."
GENERIC_ERR_MSG = ("Encountered an error. Please verify txid is correct and "
                   "try again.")

def main():
    """Get parameter and print information about tx."""
    txid = None
    if WEB_MODE:
        print "Content-Type: application/json;charset=utf-8\n"
        get_params = cgi.MiniFieldStorage()
        txid = get_params.getvalue('txid')
    else:
        try:
            txid = sys.argv[1]
        except Exception:
            pass

    if not is_txid(txid):
        print_error_msg_and_stop(INVALID_ERR_MSG)

    try:
        rpc_json = http.get_rpc_tx_json(txid)
        if bip69.is_bip69(rpc_json):
            print "{'compatible': 'true'}"
            sys.exit()
        else:
            print "{'compatible': 'false'}"
            sys.exit()
    except Exception:
        print_error_msg_and_stop(GENERIC_ERR_MSG)

def is_txid(data):
    """Determines whether data is a valid-looking txid string."""
    if not isinstance(data, str) or len(data) != TX_HASH_CHAR_LEN:
        return False
    try:
        if not all(char in string.hexdigits for char in data):
            return False
    except Exception:
        return False
    return True

def print_error_msg_and_stop(msg):
    """Print an error message and stop execution."""
    print "{'error_message':'%s'}" % msg
    sys.exit()

if __name__ == "__main__":
    main()
