#!/usr/bin/env python
#
# Copyright 2014 FreeThought Design.
#
# Licensed under the MIT license.
#
from google.appengine.ext import ndb

# Data model for probe results.
class Probe(ndb.Model):
    name = ndb.StringProperty()
    time_sent = ndb.DateTimeProperty(auto_now_add=True)
    time_rec = ndb.DateTimeProperty()
    status = ndb.IntegerProperty(default=-1)
