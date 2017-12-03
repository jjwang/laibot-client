# -*- coding: utf-8-*-
"""
A Speaker handles audio output from Jasper to the user

Speaker methods:
    say - output 'phrase' as speech
    play - play the audio in 'filename'
    is_available - returns True if the platform supports this implementation
"""
import os
import platform
import re
import tempfile
import subprocess
import pipes
import logging
import urllib
import requests
from abc import ABCMeta, abstractmethod
from uuid import getnode as get_mac  # Import for Baidu TTS

import argparse
import yaml

try:
    import gtts
except ImportError:
    pass

try:
    import pyvona
except ImportError:
    pass

from client import diagnose
from client import jasperpath


class AbstractTTSEngine(object):
    """
    Generic parent class for all speakers
    """
    __metaclass__ = ABCMeta

    @classmethod
    def get_config(cls):
        return {}

    @classmethod
    def get_instance(cls):
        config = cls.get_config()
        instance = cls(**config)
        return instance

    @classmethod
    @abstractmethod
    def is_available(cls):
        return diagnose.check_executable('aplay')

    def __init__(self, **kwargs):
        self._logger = logging.getLogger(__name__)

    @abstractmethod
    def say(self, phrase, *args):
        pass

    def play(self, filename):
        # FIXME: Use platform-independent audio-output here
        # See issue jasperproject/jasper-client#188
        cmd = ['aplay', '-D', 'plughw:1,0', str(filename)]
        self._logger.debug('Executing %s', ' '.join([pipes.quote(arg)
                                                     for arg in cmd]))
        with tempfile.TemporaryFile() as f:
            subprocess.call(cmd, stdout=f, stderr=f)
            f.seek(0)
            output = f.read()
            if output:
                self._logger.debug("Output was: '%s'", output)


class AbstractMp3TTSEngine(AbstractTTSEngine):
    """
    Generic class that implements the 'play' method for mp3 files
    """
    @classmethod
    def is_available(cls):
        return (super(AbstractMp3TTSEngine, cls).is_available() and
                diagnose.check_python_import('mad'))

    def play_mp3(self, filename):
        with tempfile.NamedTemporaryFile(suffix='.wav') as f:
            os.system('sox "%s" "%s"' % (filename, f.name))
            self.play(f.name)


class DummyTTS(AbstractTTSEngine):
    """
    Dummy TTS engine that logs phrases with INFO level instead of synthesizing
    speech.
    """

    SLUG = "dummy-tts"

    @classmethod
    def is_available(cls):
        return True

    def say(self, phrase):
        self._logger.info(phrase)

    def play(self, filename):
        self._logger.debug("Playback of file '%s' requested")
        pass


class BaiduTTS(AbstractMp3TTSEngine):
    SLUG = "baidu-tts"

    def __init__(self, api_key='', secret_key='', per=0):
        self._logger = logging.getLogger(__name__)
        self.api_key = api_key
        self.secret_key = secret_key
        self.per = per
        self.token = ''

    @classmethod
    def get_config(cls):
        # FIXME: Replace this as soon as we have a config module
        config = {}
        # Try to get baidu_yuyin config from config
        profile_path = jasperpath.config('profile.yml')
        if os.path.exists(profile_path):
            with open(profile_path, 'r') as f:
                profile = yaml.safe_load(f)
                if 'baidu_yuyin' in profile:
                    if 'api_key' in profile['baidu_yuyin']:
                        config['api_key'] = \
                            profile['baidu_yuyin']['api_key']
                    if 'secret_key' in profile['baidu_yuyin']:
                        config['secret_key'] = \
                            profile['baidu_yuyin']['secret_key']
                    if 'per' in profile['baidu_yuyin']:
                        config['per'] = \
                            profile['baidu_yuyin']['per']
        else:
            print("Cannot find config file - %s\n" % profile_path)
        return config

    @classmethod
    def is_available(cls):
        return (super(cls, cls).is_available() and
                diagnose.check_network_connection())

    def get_token(self):
        URL = 'http://openapi.baidu.com/oauth/2.0/token'
        params = urllib.parse.urlencode({'grant_type': 'client_credentials',
                                        'client_id': self.api_key,
                                         'client_secret': self.secret_key})
        r = requests.get(URL, params=params)
        try:
            r.raise_for_status()
            token = r.json()['access_token']
            return token
        except requests.exceptions.HTTPError:
            self._logger.critical('Token request failed with response: %r',
                                  r.text,
                                  exc_info=True)
            return ''

    def split_sentences(self, text):
        punctuations = ['.', '。', ';', '；', '\n']
        for i in punctuations:
            text = text.replace(i, '@@@')
        return text.split('@@@')

    def get_speech(self, phrase):
        if self.token == '':
            self.token = self.get_token()
        if self.token == '':  # Try once more
            self.token = self.get_token()
        if self.token == '':  # Try again
            self.token = self.get_token()
        query = {'tex': phrase,
                 'lan': 'zh',
                 'tok': self.token,
                 'ctp': 1,
                 'cuid': str(get_mac())[:32],
                 'per': self.per
                 }
        r = requests.post('http://tsn.baidu.com/text2audio',
                          data=query,
                          headers={'content-type': 'application/json'})
        try:
            r.raise_for_status()
            if r.json()['err_msg'] is not None:
                self._logger.critical('Baidu TTS failed with response: %r',
                                      r.json()['err_msg'],
                                      exc_info=True)
                return None
        except Exception:
            pass
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(r.content)
            tmpfile = f.name
            return tmpfile

    def say(self, phrase):
        self._logger.debug(u"Saying '%s' with '%s'", phrase, self.SLUG)
        tmpfile = self.get_speech(phrase)
        if tmpfile is not None:
            self.play_mp3(tmpfile)
            os.remove(tmpfile)


def get_default_engine_slug():
    return 'osx-tts' if platform.system().lower() == 'darwin' else 'espeak-tts'


def get_engine_by_slug(slug=None):
    """
    Returns:
        A speaker implementation available on the current platform

    Raises:
        ValueError if no speaker implementation is supported on this platform
    """

    if not slug or type(slug) is not str:
        raise TypeError("Invalid slug '%s'", slug)

    selected_filter = filter(lambda engine: hasattr(engine, "SLUG") and
                             engine.SLUG == slug, get_engines())
    selected_engines = [engine for engine in selected_filter]
    if len(selected_engines) == 0:
        raise ValueError("No TTS engine found for slug '%s'" % slug)
    else:
        if len(selected_engines) > 1:
            print("WARNING: Multiple TTS engines found for slug '%s'. " +
                  "This is most certainly a bug." % slug)
        engine = selected_engines[0]
        if not engine.is_available():
            raise ValueError(("TTS engine '%s' is not available (due to " +
                             "missing dependencies, etc.)") % slug)
        return engine


def get_engines():
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [tts_engine for tts_engine in
            list(get_subclasses(AbstractTTSEngine))
            if hasattr(tts_engine, 'SLUG') and tts_engine.SLUG]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Jasper TTS module')
    parser.add_argument('--debug', action='store_true',
                        help='Show debug messages')
    args = parser.parse_args()

    logging.basicConfig()
    if args.debug:
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

    engines = get_engines()
    available_engines = []
    for engine in get_engines():
        if engine.is_available():
            available_engines.append(engine)
    disabled_engines = list(set(engines).difference(set(available_engines)))
    print("Available TTS engines:")
    for i, engine in enumerate(available_engines, start=1):
        print("%d. %s" % (i, engine.SLUG))

    print("")
    print("Disabled TTS engines:")

    for i, engine in enumerate(disabled_engines, start=1):
        print("%d. %s" % (i, engine.SLUG))

    print("")
    for i, engine in enumerate(available_engines, start=1):
        print("%d. Testing engine '%s'..." % (i, engine.SLUG))
        engine.get_instance().say("This is a test.")

    print("Done.")
