import urllib2
import ssl
from socket import error as SocketError
import os
import ConfigParser
import json

ENABLE_DEBUG_PRINT = False

TX_BASE_URL         = "https://blockchain.info/tx/"
TX_INDEX_BASE_URL   = "https://blockchain.info/tx-index/"
SATOSHIS_PER_BTC = 100000000

CONFIG_FILENAME = 'app.cfg'

MAX_RETRY_TIME_IN_SEC = 60
NUM_SEC_TIMEOUT = 30
NUM_SEC_SLEEP = 0

def fetch_url(url):
    """Fetch contents of remote page as string for specified url."""

    if NUM_SEC_SLEEP > 0:
        time.sleep(NUM_SEC_SLEEP)

    current_retry_time_in_sec = 0

    dprint("Fetching url: %s" % url)

    response = ''
    while current_retry_time_in_sec <= MAX_RETRY_TIME_IN_SEC:
        if current_retry_time_in_sec:
            time.sleep(current_retry_time_in_sec)
        try:
            response = urllib2.urlopen(url=url, timeout=NUM_SEC_TIMEOUT).read()
            if response is None:
                #For some reason, no handler handled the request
                raise Exception
            return response
        except (urllib2.HTTPError, ssl.SSLError) as err:
            #There was a problem fetching the page, maybe something other than
            #   HTTP 200 OK.
            if current_retry_time_in_sec == MAX_RETRY_TIME_IN_SEC:
                raise Exception
            else:
                current_retry_time_in_sec = current_retry_time_in_sec + 1
                dprint(("Encountered HTTPError fetching '%s'. Will waiting for "
                        "%d seconds before retrying. Error was: '%s'") %
                       (url, current_retry_time_in_sec, str(err)))
        except urllib2.URLError as err:
            if current_retry_time_in_sec == MAX_RETRY_TIME_IN_SEC:
                raise Exception
            else:
                current_retry_time_in_sec = current_retry_time_in_sec + 1
                dprint(("Encountered URLError fetching '%s'. Will waiting for "
                        "%d seconds before retrying. Error was: '%s'") %
                       (url, current_retry_time_in_sec, str(err)))
        except SocketError as err:
            if current_retry_time_in_sec == MAX_RETRY_TIME_IN_SEC:
                raise Exception
            else:
                current_retry_time_in_sec = current_retry_time_in_sec + 1
                dprint(("Encountered SocketErr fetching '%s'. Will waiting for "
                        "%d seconds before retrying. Error was: '%s'") %
                       (url, current_retry_time_in_sec, str(err)))

def api_key_from_cfg():
    """Returns API key or None if not set in config file.

    Config file should look like:
        [API]
        key=my_secret_blockchain_info_API_key_permitting_faster_requests
    """
    config_parser = ConfigParser.ConfigParser()
    try:
        config_parser.read(CONFIG_FILENAME)
        return config_parser.get(section='API', option='key')
    except ConfigParser.Error:
        return None

def build_tx_url(txid, api_key=None):
    """Build the URL needed to get data for specified transaction"""
    url = "%s%s?format=json" % (TX_BASE_URL, txid)
    if api_key is None:
        api_key = api_key_from_cfg()
    if api_key is not None:
        url = "%s&api_code=%s" % (url, api_key)
    return url

def build_tx_index_url(tx_index, api_key=None):
    """Build the URL needed to get data for specified previous tx output.
    Args:
        tx_index: The transaction index as string or integer.
    Returns:
        str: URL.
    """
    url = "%s%s?format=json" % (TX_INDEX_BASE_URL, str(tx_index))
    if api_key is None:
        api_key = api_key_from_cfg()
    if api_key is not None:
        url = "%s&api_code=%s" % (url, api_key)
    return url

def get_rpc_tx_json(txid):
    """Given a txid, request data from BC.I until we have an RPC-like JSON.

    Data includes:
        * txid
        * vin (list)
            * txid
            * vout
        * vout (list)
            * value (in BTC)
            * scriptPubKey
                * hex

    Args:
        txid (str): 64-character hex string representing hash of tx. Validation
            of the string is the responsibility of the caller.
    Returns:
        JSON object combatible with data returned from bitcoind's
        `decoderawtransaction`, or an empty object if not obtainable.
    """

    bci_tx_json = json.loads(fetch_url(build_tx_url(txid)))
    rpc_json = {'txid':txid, 'vin': [], 'vout':[]}
    if 'inputs' not in bci_tx_json or 'out' not in bci_tx_json:
        dprint("'inputs' or 'out' field not found for tx %s" % txid)
        return {} #something missing from BCI's JSON
    for tx_input in bci_tx_json['inputs']:
        if 'prev_out' not in tx_input or 'tx_index' not in tx_input['prev_out']:
            dprint("'tx_index' field not found for one of inputs in tx %s" %
                   txid)
            continue
        tx_index = tx_input['prev_out']['tx_index']
        tx_index_json = json.loads(fetch_url(build_tx_index_url(tx_index)))
        prev_txid = tx_index_json['hash']
        vout = tx_input['prev_out']['n']
        vin = {'txid':prev_txid, 'vout':vout}
        rpc_json['vin'].append(vin)
    for tx_output in bci_tx_json['out']:
        if 'value' not in tx_output or 'script' not in tx_output:
            continue
        value = float(tx_output['value']) / SATOSHIS_PER_BTC
        script_pub_key_hex = tx_output['script']
        vout = {'value':value, 'scriptPubKey':{'hex':script_pub_key_hex}}
        rpc_json['vout'].append(vout)
    return rpc_json

def dprint(msg):
    """Debug print statements."""
    if ENABLE_DEBUG_PRINT:
        print "DEBUG: %s" % msg
