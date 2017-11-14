# -*- coding: utf-8-*-
from sys import maxint
import random
import sys # Laibot
import urllib, urllib2
import re

reload(sys)
sys.setdefaultencoding('utf8')

WORDS = []

PRIORITY = -(maxint + 1)


def handle(text, mic, profile):
    """
        Reports that the user has unclear or unusable input.

        Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """

    try:
        url = 'http://laibot.applinzi.com/chat?'
        req = re.sub('[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@]'.decode('utf8'), ''.decode('utf8'), text)
        url = url + urllib.urlencode({'req': req})
        http_response = urllib2.urlopen(urllib2.Request(url))
        mic.say(http_response.read())
    except Exception as err:
        print(str(err))

        messages = ["我没有听清楚",
                    "请再说一遍"]
        message = random.choice(messages)
        mic.say(message)


def isValid(text):
    return True
