'''Unit tests for `bip69` module.'''

import unittest
import json

import bip69 #bip69.py

class Bip69Test(unittest.TestCase):
    """Ensure `bip69` module is working correctly."""

    def setUp(self):
        """Open JSON files from disk."""
        with open('test/0a6a357e.json') as read_file:
            self.tx_json_0a6a357e = json.load(read_file)
        with open('test/bip69-synth.json') as read_file:
            self.bip69_synth = json.load(read_file)

    def test_get_inputs_from_rpc_json_0a6a357e(self):
        """Verify that relevant input data is extracted for tx 0a6a357e..."""
        inputs = bip69.get_inputs_from_rpc_json(self.tx_json_0a6a357e)

        self.assertEqual(len(inputs), 17)
        self.assertEqual(inputs[0], (('643e5f4e66373a57251fb173151e838ccd27d279'
                                      'aca882997e005016bb53d5aa'), 0))
        self.assertEqual(inputs[15], (('6c1d56f31b2de4bfc6aaea28396b333102b1f60'
                                       '0da9c6d6149e96ca43f1102b1'), 1))

    def test_sort_inputs_0a6a357e(self):
        """Verify that inputs are correctly sorted for tx 0a6a357e..."""
        inputs = bip69.get_inputs_from_rpc_json(self.tx_json_0a6a357e)
        bip69_inputs = bip69.sort_inputs(inputs)
        self.assertEqual(bip69_inputs[0],
                         (('0e53ec5dfb2cb8a71fec32dc9a634a35b7e24799295ddd52782'
                           '17822e0b31f57'), 0))
        self.assertEqual(bip69_inputs[10],
                         (('7d037ceb2ee0dc03e82f17be7935d238b35d1deabf953a892a4'
                           '507bfbeeb3ba4'), 1))

    def test_get_outputs_from_rpc_json_0a6a357e(self):
        """Verify that relevant output data is extracted for tx 0a6a357e..."""
        outputs = bip69.get_outputs_from_rpc_json(self.tx_json_0a6a357e)

        self.assertEqual(len(outputs), 2)
        self.assertEqual(outputs[0], (('76a9144a5fba237213a062f6f57978f796390bd'
                                       'cf8d01588ac'), 400057456))
        self.assertEqual(outputs[1], (('76a9145be32612930b8323add2212a4ec03c156'
                                       '2084f8488ac'), 40000000000))

    def test_sort_outputs_0a6a357e(self):
        """Verify that outputs are correctly sorted for tx 0a6a357e..."""
        outputs = bip69.get_outputs_from_rpc_json(self.tx_json_0a6a357e)
        bip69_outputs = bip69.sort_outputs(outputs)
        self.assertEqual(bip69_outputs[0], (('76a9144a5fba237213a062f6f57978f79'
                                             '6390bdcf8d01588ac'), 400057456))
        self.assertEqual(bip69_outputs[1], (('76a9145be32612930b8323add2212a4ec'
                                             '03c1562084f8488ac'), 40000000000))

    def test_is_bip69_0a6a357e(self):
        """Test a transaction that isn't bip-69 compliant"""
        self.assertFalse(bip69.is_bip69(self.tx_json_0a6a357e))

    def test_is_bip69_with_properly_sorted_inputs_and_outputs(self):
        """Test a synthesized transaction that is BIP-69 compliant."""
        self.assertTrue(bip69.is_bip69(self.bip69_synth))

unittest.TestLoader().loadTestsFromTestCase(Bip69Test)
