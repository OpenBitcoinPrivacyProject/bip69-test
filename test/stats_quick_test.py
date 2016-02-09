"""Unit tests for the `stats` module using bitcoind's RPC interface."""
import unittest
import bitcoind_rpc #bitcoind_rpc.py
import stats #stats.py

class StatsTest(unittest.TestCase):
    """A few slow tests for the `stats` module."""
    def setUp(self):
        """Set up test."""
        self.conn = bitcoind_rpc.RPCConnection()

    def tearDown(self):
        """Finish test."""
        self.conn = None

    def test_percent_per_block_genesis(self):
        """100% of genesis block is compliant (coinbase only)"""
        compliant_pct = stats.percent_compliant_per_block(block_height=0,
                                                          rpc_conn=self.conn)
        self.assertEqual(compliant_pct, 1.0)

    def test_percent_per_block_partial(self):
        """60% of transactions at height 100012 are compliant"""
        compliant_pct = stats.percent_compliant_per_block(block_height=100012,
                                                          rpc_conn=self.conn)
        self.assertEqual(compliant_pct, 4.0/6)

unittest.TestLoader().loadTestsFromTestCase(StatsTest)
