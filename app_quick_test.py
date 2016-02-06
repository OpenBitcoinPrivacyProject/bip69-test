import unittest
import app
import http

class AppTest(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_is_txid(self):

        good1 = ('1234567890123456789012345678901234567890123456789012345678901'
                 '234')
        good2 = ('1234567890abcdef1234567890abcdef1234567890abcdef1234567890abc'
                 'def')
        bad1 = '1234abcd'
        bad2 = ('12345678901234567890123456789012345678901234567890123456789012'
                 '3x')
        self.assertTrue(app.is_txid(good1))
        self.assertTrue(app.is_txid(good2))
        self.assertFalse(app.is_txid(bad1))
        self.assertFalse(app.is_txid(bad2))

unittest.TestLoader().loadTestsFromTestCase(AppTest)
