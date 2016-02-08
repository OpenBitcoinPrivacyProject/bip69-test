"""Unit tests for the `stats` module requiring http responses."""
import unittest
import stats #stats.py

class StatsTest(unittest.TestCase):
    """A few slow tests for the `stats` module."""

    def test_percent_per_block_genesis(self):
        """100% of genesis block is compliant (coinbase only)"""
        compliant_pct = stats.percent_compliant_per_block(block_height=0)
        self.assertEqual(compliant_pct, 1.0)

    def test_percent_per_block_partial(self):
        """60% of transactions at height 100012 are compliant"""
        compliant_pct = stats.percent_compliant_per_block(block_height=100012)
        self.assertEqual(compliant_pct, 4.0/6)

unittest.TestLoader().loadTestsFromTestCase(StatsTest)
