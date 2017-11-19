#!/usr/bin/env python2
# -*- coding: utf-8-*-
import unittest
from client import test_mic
from client.modules import Unclear

DEFAULT_PROFILE = {
    'prefers_email': False,
    'location': 'Cape Town',
    'timezone': 'US/Eastern',
    'phone_number': '012344321'
}


class TestModules(unittest.TestCase):

    def setUp(self):
        self.profile = DEFAULT_PROFILE
        self.send = False

    def runConversation(self, query, inputs, module):
        """Generic method for spoofing conversation.

        Arguments:
        query -- The initial input to the server.
        inputs -- Additional input, if conversation is extended.

        Returns:
        The server's responses, in a list.
        """
        self.assertTrue(module.isValid(query))
        mic = test_mic.Mic(inputs)
        module.handle(query, mic, self.profile)
        return mic.outputs

    def testUnclear(self):
        query = "What time is it?"
        inputs = []
        self.runConversation(query, inputs, Unclear)
