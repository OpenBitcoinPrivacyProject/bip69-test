"""Takes care of fetching data via HTTP."""
import urllib2
import ssl
from socket import error as SocketError
import ConfigParser
import json
import time

ENABLE_DEBUG_PRINT = False

TX_BASE_URL = "https://blockchain.info/tx/"
TX_INDEX_BASE_URL = "https://blockchain.info/tx-index/"
BLOCK_HEIGHT_BASE_URL = "https://blockchain.info/block-height/"
SATOSHIS_PER_BTC = 100000000

CONFIG_FILENAME = 'app.cfg'

MAX_RETRY_TIME_IN_SEC = 2
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

def get_url_with_api_key(url, api_key):
    """Adds the API key to the url as param if specified.
    Args:
        url (str): The base URL.
        api_key (str or None): API key.
    Returns:
        str: URL.
    """
    if api_key is None:
        api_key = api_key_from_cfg()
    if api_key is not None:
        url = "%s&api_code=%s" % (url, api_key)
    return url

def build_tx_url(txid, api_key=None):
    """Build the URL needed to get data for specified transaction"""
    url = "%s%s?format=json" % (TX_BASE_URL, txid)
    return get_url_with_api_key(url, api_key)

def build_tx_index_url(tx_index, api_key=None):
    """Build the URL needed to get data for specified previous tx output.
    Args:
        tx_index: The transaction index as string or integer.
    Returns:
        str: URL.
    """
    url = "%s%s?format=json" % (TX_INDEX_BASE_URL, str(tx_index))
    return get_url_with_api_key(url, api_key)

def build_block_url(block_height, api_key=None):
    """Build the URL needed to get data for specified block.
    Args:
        block_height: Integer greater than or equal to zero.
    Returns:
        str: URL.
    """
    url = "%s%d?format=json" % (BLOCK_HEIGHT_BASE_URL, block_height)
    return get_url_with_api_key(url, api_key)

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

def get_block_txids(block_height):
    """Get a list of transaction ids as base58 strings for the block height."""
    assert isinstance(block_height, int)
    assert block_height >= 0

    bci_blocks_json = json.loads(fetch_url(build_block_url(block_height)))
    main_chain_block = get_main_chain_block(bci_blocks_json)
    txids = []
    for txn in main_chain_block['tx']:
        if 'hash' in txn:
            txids.append(txn['hash'])
    return txids

def get_main_chain_block(bci_blocks_json):
    """Get the block that belongs to the Bitcoin main chain.
    BC.I's /block_height end point will return a list of blocks in JSON format,
    but only one of them will be the main chain block, with others having been
    orphaned.
    Args:
        bci_blocks_json: The object returned by calling `json.loads` on
            BC.I's /block-height endpoint at a specified height.
    Returns:
        JSON object consisting of a single block's worth of information.
    """
    for block in bci_blocks_json['blocks']:
        if block['main_chain']:
            return block
    raise Exception

def dprint(msg):
    """Debug print statements."""
    if ENABLE_DEBUG_PRINT:
        print "DEBUG: %s" % msg
