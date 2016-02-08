"""Calculate stats about BIP-69 compliance"""

import sys
import http #http.py
import bip69 #bip69.py

def percent_compliant_per_block(block_height):
    """Returns % of transactions in block that are compliant, as float."""
    assert isinstance(block_height, int)
    assert block_height >= 0

    txids = http.get_block_txids(block_height)
    num_compliant = 0
    for txid in txids:
        rpc_tx_json = http.get_rpc_tx_json(txid)
        if bip69.is_bip69(rpc_tx_json):
            num_compliant = num_compliant + 1
    return float(num_compliant) / len(txids)

def main():
    min_block_height = int(sys.argv[1])
    max_block_height = int(sys.argv[2])
    num_blocks = max_block_height - min_block_height + 1
    total = 0.0
    for block_height in range(min_block_height, max_block_height+1):
        pct = percent_compliant_per_block(block_height)
        print "\t%d,%f" % (block_height, pct)
        total = total + pct
    avg = total / num_blocks
    print "avg compliance: %f" % avg

if __name__ == "__main__":
    main()
