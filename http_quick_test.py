import unittest
import http

class HttpTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_build_tx_url(self):
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
        ##https://blockchain.info/tx-index/50555080?format=json
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

unittest.TestLoader().loadTestsFromTestCase(HttpTest)
