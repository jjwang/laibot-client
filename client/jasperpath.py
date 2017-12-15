# -*- coding: utf-8-*-
import os

# Jasper main directory
APP_PATH = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))

DATA_PATH = os.path.join(APP_PATH, "static")
LIB_PATH = os.path.join(APP_PATH, "client")
TOOLS_PATH = os.path.join(APP_PATH, "tools")

PLUGIN_PATH = os.path.join(LIB_PATH, "modules")
CONFIG_PATH = os.path.join(APP_PATH, 'conf')
TJBOT_PATH = os.path.join(APP_PATH, '../tjbot/bootstrap/tests/')


def config(*fname):
    return os.path.join(CONFIG_PATH, *fname)


def data(*fname):
    return os.path.join(DATA_PATH, *fname)


def tjbot(*fname):
    return os.path.join(TJBOT_PATH, *fname)
