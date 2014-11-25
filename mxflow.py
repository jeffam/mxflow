#!/usr/bin/env python
#
# Copyright 2014 FreeThought Design.
#
# Licensed under the MIT license.
#
import os, re, ConfigParser

def getVersion():
    return os.environ['CURRENT_VERSION_ID'].split('.')[0].replace('-', '.')

def getConfig():
    confdict = {}
    config = ConfigParser.ConfigParser()
    config.read("config.ini")

    for section in config.sections():
        confdict[section] = {}
        for key, val in config.items(section):
            confdict[section][key] = val

    return confdict
