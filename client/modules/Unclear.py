# -*- coding: utf-8-*-
import random
import sys  # Laibot
import urllib
import re
import os
import client.jasperpath as jasperpath

WORDS = []

PRIORITY = -(sys.maxsize + 1)


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
        pat = '[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@]'
        req = re.sub(pat, '', text)
        url = url + urllib.parse.urlencode({'req': req})
        http_response = urllib.request.urlopen(url)
        ans = http_response.read().decode('utf-8')
        if ans.find('//shakehand') >= 0:
            ans = ans.replace('//shakehand', '')
            if os.path.exists(jasperpath.tjbot('shakehand.servo.js')):
                os.system("node " + jasperpath.tjbot('shakehand.servo.js'))
                os.system("node " + jasperpath.tjbot('shakehand.servo.js'))
        mic.say(ans)
    except Exception as err:
        print(str(err))

        messages = ["我没有听清楚",
                    "请再说一遍"]
        message = random.choice(messages)
        mic.say(message)


def isValid(text):
    return True
