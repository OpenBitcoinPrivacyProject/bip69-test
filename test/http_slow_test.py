"""Unit tests for the `http` module that involve waiting for http responses."""
import unittest
import json
import http #http.py

class HttpTest(unittest.TestCase):
    """A few slow tests for the `http` module."""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_fetch_url_valid(self):
        '''Requires remote host to be accessible and responsive.'''
        txid = ('15796981d90b9ecbce09a9e8a7b4f447566f2f859b808f4e940fb3b6ac17d3'
                'd5')
        url = http.build_tx_url(txid)
        response = http.fetch_url(url)
        json_obj = json.loads(response)
        self.assertEqual(json_obj['ver'], 1)

    def test_get_rpc_tx_json(self):
        '''Make sure that data for tx 15796981... is properly formatted.'''
        txid = ('15796981d90b9ecbce09a9e8a7b4f447566f2f859b808f4e940fb3b6ac17d3'
                'd5')
        rpc_json = http.get_rpc_tx_json(txid)
        self.assertIn('txid', rpc_json)
        self.assertEqual(rpc_json['txid'], txid)
        self.assertIn('vin', rpc_json)
        self.assertEqual(len(rpc_json['vin']), 4)
        self.assertEqual(rpc_json['vin'][0]['txid'],
                         ('916d81523a14bb9690f112afe1447893abd8ba4180af855ef4b1'
                          '7f336af3ba33'))
        self.assertEqual(rpc_json['vin'][0]['vout'], 0)
        self.assertEqual(rpc_json['vin'][1]['txid'],
                         ('35ca713f844b6041840ffd89836dd19a3a6add27b2ca45a49c89'
                          '7d75991d04f3'))
        self.assertEqual(rpc_json['vin'][1]['vout'], 0)
        self.assertEqual(rpc_json['vin'][2]['txid'],
                         ('87e73af7a2084d28a803de8817cfccd15cbd3573d21f70adef6d'
                          '825a5a702565'))
        self.assertEqual(rpc_json['vin'][2]['vout'], 0)
        self.assertEqual(rpc_json['vin'][3]['txid'],
                         ('00ec11a92c6b9c1aa4d9cf11c0b655014ba886d1abed3b14a5f3'
                          'b185e2e842ac'))
        self.assertEqual(rpc_json['vin'][3]['vout'], 4)
        self.assertIn('vout', rpc_json)
        self.assertEqual(len(rpc_json['vout']), 4)
        self.assertEqual(rpc_json['vout'][0]['value'], 0.02500000)
        self.assertEqual(rpc_json['vout'][0]['scriptPubKey']['hex'],
                         '76a914e364c1eeded620aaa98681e63f59bab28d7aa29f88ac')
        self.assertEqual(rpc_json['vout'][1]['value'], 0.23100000)
        self.assertEqual(rpc_json['vout'][1]['scriptPubKey']['hex'],
                         '76a914ab65580854ae75de97c1e51ad034a1885942054d88ac')
        self.assertEqual(rpc_json['vout'][2]['value'], 0.51000000)
        self.assertEqual(rpc_json['vout'][2]['scriptPubKey']['hex'],
                         '76a9141226fb5ca7bed350ea7d3651b104e2981177675b88ac')
        self.assertEqual(rpc_json['vout'][3]['value'], 0.63502445)
        self.assertEqual(rpc_json['vout'][3]['scriptPubKey']['hex'],
                         '76a9149c2280c4b6bc685ea756ee6dc1d56e34aea2ecae88ac')

    def test_get_block_txids(self):
        """Verify that a block height is correctly fetched."""
        block_height = 187
        txids = http.get_block_txids(block_height)
        self.assertEqual(len(txids), 2)
        self.assertIn(('70587f1780ccd2ebbace28a7b33d83d19f4362f10ff7a4ad88f8c41'
                       '3883f94b7'), txids)
        self.assertIn(('4385fcf8b14497d0659adccfe06ae7e38e0b5dc95ff8a13d7c62035'
                       '994a0cd79'), txids)

unittest.TestLoader().loadTestsFromTestCase(HttpTest)
