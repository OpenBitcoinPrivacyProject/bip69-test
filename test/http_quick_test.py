"""Unit tests for `http` module that don't require network traffic."""

import unittest
import http
import json

class HttpTest(unittest.TestCase):
    """Quick testss for functions in `http` module."""
    def test_build_tx_url(self):
        """Build one URL to fetch tx data from blockchain.info."""
        txid = ('15796981d90b9ecbce09a9e8a7b4f447566f2f859b808f4e940fb3b6ac17d3'
                'd5')
        url = http.build_tx_url(txid)

        self.assertIn(
            ('https://blockchain.info/tx/15796981d90b9ecbce09a9e8a7b4f447566f2f'
             '859b808f4e940fb3b6ac17d3d5?format=json'),
            url,
            'should be valid url + optional api code set in cfg file.')
        api_key = 'scoobydoo'
        url = http.build_tx_url(txid=txid, api_key=api_key)
        self.assertEqual(url,
                         ('https://blockchain.info/tx/15796981d90b9ecbce09a9e8a'
                          '7b4f447566f2f859b808f4e940fb3b6ac17d3d5?'
                          'format=json&api_code=scoobydoo'),
                         'should be valid url using specified api code.')

    def test_build_tx_index_url(self):
        """Build one URL to fetch previous output data from blockchain.info."""
        tx_index = '50555080'
        url = http.build_tx_index_url(tx_index)
        self.assertIn(
            'https://blockchain.info/tx-index/50555080?format=json', url,
            'should be valid url + optional api code set in cfg file.')

        api_key = 'scrappydoo'
        url = http.build_tx_index_url(tx_index=tx_index, api_key=api_key)
        self.assertEqual(url,
                         ('https://blockchain.info/tx-index/50555080?'
                          'format=json&api_code=scrappydoo'),
                         'should be valid url using specified api code.')

    def test_build_block_url(self):
        """Build one URL to fetch block data from blockchain.info"""
        block_height = 187
        url = http.build_block_url(block_height)
        self.assertIn(
            'https://blockchain.info/block-height/187?format=json',
            url,
            'should be a valid url + optional api code set in cfg file.')
        api_key = 'scrappydoo'
        url = http.build_block_url(block_height=block_height, api_key=api_key)
        self.assertEqual(
            url,
            ('https://blockchain.info/block-height/187?format=json'
             '&api_code=scrappydoo'),
            'should be valid url using specified api code.')

    def test_get_main_chain_block(self):
        """Verify that the correct block is extracted from a list."""
        fake_json_str = """
        {
            "blocks": [
                {
                    "hash": "cd",
                    "main_chain": false
                },
                {
                    "hash": "ab",
                    "main_chain": true
                }
            ]
        }
        """
        fake_json = json.loads(fake_json_str)
        block = http.get_main_chain_block(bci_blocks_json=fake_json)
        self.assertTrue(block['hash'], 'ab')

unittest.TestLoader().loadTestsFromTestCase(HttpTest)
