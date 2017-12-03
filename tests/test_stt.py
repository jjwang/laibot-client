#!/usr/bin/env python2
# -*- coding: utf-8-*-
import unittest
import imp
from client import stt, jasperpath


def cmuclmtk_installed():
    try:
        imp.find_module('cmuclmtk')
    except ImportError:
        return False
    else:
        return True


def pocketsphinx_installed():
    try:
        imp.find_module('pocketsphinx')
    except ImportError:
        return False
    else:
        return True


@unittest.skipUnless(cmuclmtk_installed(), "CMUCLMTK not present")
@unittest.skipUnless(pocketsphinx_installed(), "Pocketsphinx not present")
class TestSTT(unittest.TestCase):

    def setUp(self):
        self.jasper_clip = jasperpath.data('audio', 'jasper.wav')
        self.weather_zh_clip = jasperpath.data('audio', 'weather_zh.wav')

        self.passive_stt_engine = stt.PocketSphinxSTT.get_passive_instance()
        self.active_stt_engine = stt.BaiduSTT.get_active_instance()

    def testTranscribeJasper(self):
        """
        Does Jasper recognize his name (i.e., passive listen)?
        """
        with open(self.jasper_clip, mode="rb") as f:
            transcription = self.passive_stt_engine.transcribe(f)
        self.assertIn("JASPER", transcription)

    def testTranscribe(self):
        """
        Does Jasper recognize '今天的天气' (i.e., active listen)?
        """
        pass
        with open(self.weather_zh_clip, mode="rb") as f:
            transcription = self.active_stt_engine.transcribe(f)
        self.assertIn("今天的天气", transcription[0][0:15])
