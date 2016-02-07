"""Unit tests for the main module, `app`. Tests in command-line mode.

In order to put `app.py` into command-line mode, temporarily set its `WEB_MODE`
flag to `True`.
"""

import commands
import unittest
import app #app.py

BIP_69_VALID_JSON = "{'compatible': 'true'}"
BIP_69_INVALID_JSON = "{'compatible': 'false'}"

class AppTest(unittest.TestCase):
    """A series of tests, most of which involve network queries."""
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_main_empty_txid(self):
        '''Should get an error message.'''
        txid = ''
        output = commands.getoutput('python app.py %s' % txid)
        self.assertEqual(output, "{'error_message':'%s'}" % app.INVALID_ERR_MSG)

    def test_main_txid_too_short(self):
        '''Should get an error message.'''
        txid = '0123456789abcdef'
        output = commands.getoutput('python app.py %s' % txid)
        self.assertEqual(output, "{'error_message':'%s'}" % app.INVALID_ERR_MSG)

    def test_main_txid_too_long(self):
        '''Should get an error message.'''
        txid = ('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcd'
                'ef0')
        output = commands.getoutput('python app.py %s' % txid)
        self.assertEqual(output, "{'error_message':'%s'}" % app.INVALID_ERR_MSG)

    def test_tx_doesntexist(self):
        '''Should get a generic error message.'''
        txid = ('0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcd'
                'ef')
        output = commands.getoutput('python app.py %s' % txid)
        self.assertEqual(output, "{'error_message':'%s'}" % app.GENERIC_ERR_MSG)

    def test_tx_not_bip69(self):
        """A random tx that isn't bip-69 compliant. Results in generic err."""
        txid = ('15796981d90b9ecbce09a9e8a7b4f447566f2f859b808f4e940fb3b6ac17d3'
                'd5')
        output = commands.getoutput('python app.py %s' % txid)
        self.assertEqual(output, BIP_69_INVALID_JSON)

    def test_bip69_coinbase_tx(self):
        '''This is bip69 as it has no inputs and only one output.'''
        txid = ('19fc580bacfe0598a2c1c3bbf08af6defc760e45a51671adf7992470def2a0'
                'd9')
        output = commands.getoutput('python app.py %s' % txid)
        self.assertEqual(output, BIP_69_VALID_JSON)

    def test_bip69_one_input_and_output(self):
        '''This is bip69 as it has one input and one output.'''
        txid = ('96b36ceb07d3408beae11a76f786f9d30352055a0be8167fbd691d697c4b16'
                '3b')
        output = commands.getoutput('python app.py %s' % txid)
        self.assertEqual(output, BIP_69_VALID_JSON)

    def test_bip69_multi_output(self):
        '''This is coincidentally bip69 compliant.

        output 0: 0.014663 BTC
        output 1: 0.126627 BTC
        '''
        txid = ('0afa520fd1d5c36d026556599de455946608a8f1908ddc02db8da5fd96a256'
                '51')
        output = commands.getoutput('python app.py %s' % txid)
        self.assertEqual(output, BIP_69_VALID_JSON)

unittest.TestLoader().loadTestsFromTestCase(AppTest)
