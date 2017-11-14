#!/usr/bin/env python2
# -*- coding: utf-8-*-
import unittest
import mock
from client import brain, test_mic


DEFAULT_PROFILE = {
    'prefers_email': False,
    'location': 'Cape Town',
    'timezone': 'US/Eastern',
    'phone_number': '012344321'
}


class TestBrain(unittest.TestCase):

    @staticmethod
    def _emptyBrain():
        mic = test_mic.Mic([])
        profile = DEFAULT_PROFILE
        return brain.Brain(mic, profile)

    def testLog(self):
        """Does Brain correctly log errors when raised by modules?"""
        my_brain = TestBrain._emptyBrain()
        unclear = my_brain.modules[-1]
        with mock.patch.object(unclear, 'handle') as mocked_handle:
            with mock.patch.object(my_brain._logger, 'error') as mocked_log:
                mocked_handle.side_effect = KeyError('foo')
                my_brain.query("zzz gibberish zzz")
                self.assertTrue(mocked_log.called)

    def testSortByPriority(self):
        """Does Brain sort modules by priority?"""
        my_brain = TestBrain._emptyBrain()
        priorities = filter(lambda m: hasattr(m, 'PRIORITY'), my_brain.modules)
        target = sorted(priorities, key=lambda m: m.PRIORITY, reverse=True)
        self.assertEqual(target, priorities)
