'''Unit tests for `bitcoind_rpc` module.'''

import unittest
import bitcoind_rpc #bitcoind_rpc.py

BLOCK_170_HASH = ('00000000d1145790a8694403d4063f323d499e655c83426834d4ce2f8dd4'
                  'a2ee')

class RPCTest(unittest.TestCase):
    """Ensure `bitcoind_rpc` module is working correctly."""

    def setUp(self):
        """Set up test."""
        self.conn = bitcoind_rpc.RPCConnection()

    def tearDown(self):
        """Finish test."""
        self.conn = None

    def test_init(self):
        """Verify that `__init__` appears to work."""
        self.assertIsNotNone(self.conn)

    def test_get_block_hash_at_height(self):
        """Verify the block hash is correct for block 170."""
        block_hash = self.conn.get_block_hash_at_height(170)
        self.assertEqual(block_hash, BLOCK_170_HASH)

    def test_get_json_for_block_hash(self):
        """Verify we can fetch block's JSON representation."""
        block_json = self.conn.get_json_for_block_hash(BLOCK_170_HASH)
        self.assertEqual(block_json['hash'], BLOCK_170_HASH)
        self.assertEqual(block_json['height'], 170)

    def test_get_tx_ids_at_height(self):
        """Verify we can fetch transaction ids for specified block height."""
        txids = self.conn.get_tx_ids_at_height(170)
        self.assertEqual(len(txids), 2)
        self.assertIn(
            'b1fea52486ce0c62bb442b530a3f0132b826c74e473d1f2c220bfa78111c5082',
            txids)
        self.assertIn(
            'f4184fc596403b9d638783cf57adfe4c75c605f6356fbc91338530e9831e9e16',
            txids)

    def test_get_raw_tx(self):
        """Verify we can get a raw transaction from RPC interface."""
        raw_tx = self.conn.get_raw_tx(
            'b1fea52486ce0c62bb442b530a3f0132b826c74e473d1f2c220bfa78111c5082')
        self.assertEqual(
            raw_tx,
            ('01000000010000000000000000000000000000000000000000000000000000000'
            '000000000ffffffff0704ffff001d0102ffffffff0100f2052a01000000434104d'
            '46c4968bde02899d2aa0963367c7a6ce34eec332b32e42e5f3407e052d64ac625d'
             'a6f0718e7b302140434bd725706957c092db53805b821a85b23a7ac61725bac00'
             '000000'))

    def test_get_decoded_tx(self):
        """Verify that we can get a transaction in JSON format."""
        tx_json = self.conn.get_decoded_tx(
            'b1fea52486ce0c62bb442b530a3f0132b826c74e473d1f2c220bfa78111c5082')
        self.assertEqual(
            tx_json['txid'],
            'b1fea52486ce0c62bb442b530a3f0132b826c74e473d1f2c220bfa78111c5082')
        self.assertEqual(tx_json['vin'][0]['coinbase'], '04ffff001d0102')

unittest.TestLoader().loadTestsFromTestCase(RPCTest)
