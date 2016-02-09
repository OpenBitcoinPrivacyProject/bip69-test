"""Calculate stats about BIP-69 compliance"""

import sys
import http #http.py
import bip69 #bip69.py
import bitcoind_rpc #bitcoind_rpc.py

def percent_compliant_per_block(block_height, rpc_conn=None):
    """Returns % of transactions in block that are compliant, as float.

    Args:
        block_height (int): Height of block requested.
        rpc_conn (Optional[`bitoind_rpc.RPCConnection`]): A connection class
            to the bitcoind RPC interface for local fetching of blockchain data.
    """
    assert isinstance(block_height, int)
    assert block_height >= 0

    txids = None
    if rpc_conn is not None:
        txids = rpc_conn.get_tx_ids_at_height(block_height)
    else:
        txids = http.get_block_txids(block_height)
    num_compliant = 0
    for txid in txids:
        rpc_tx_json = None
        if rpc_conn is not None:
            rpc_tx_json = rpc_conn.get_decoded_tx(txid)
        else:
            rpc_tx_json = http.get_rpc_tx_json(txid)
        if bip69.is_bip69(rpc_tx_json):
            num_compliant = num_compliant + 1
    return float(num_compliant) / len(txids)

def main():
    """Main.

    Usage:
    $ python stats.py min_block_height [max_block_height] [1|0]
    Last argument is whether to use bitcoind's local RPC connection instead of
        a block explorer API.
    """
    min_block_height = int(sys.argv[1])
    max_block_height = min_block_height
    if len(sys.argv) > 2:
        max_block_height = int(sys.argv[2])
    rpc_conn = None
    if len(sys.argv) > 3 and int(sys.argv[3]) == 1:
        rpc_conn = bitcoind_rpc.RPCConnection()

    num_blocks = max_block_height - min_block_height + 1
    total = 0.0
    for block_height in range(min_block_height, max_block_height+1):
        pct = percent_compliant_per_block(block_height, rpc_conn)
        print "\t%d,%f" % (block_height, pct)
        total = total + pct
    avg = total / num_blocks
    print "avg compliance: %f" % avg

if __name__ == "__main__":
    main()
