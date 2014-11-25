#!/usr/bin/env python
#
# Copyright 2014 FreeThought Design.
#
# Licensed under the MIT license.
#
import logging, webapp2, mxflow
from datetime import datetime
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.ext import ndb
from google.appengine.api import mail
from models import *

class LogSenderHandler(InboundMailHandler):
    def receive(self, mail_message):
        logging.info("Got me a message from: " + mail_message.sender)

        try:
            probe_key = ndb.Key(urlsafe=mail_message.subject)
        except:
            logging.info('bad key')
        else:
            # TODO: Don't accept replies for timed-out probes.
            logging.info(probe_key)
            probe = probe_key.get()
            probe.time_rec = datetime.now()
            probe.status = 1
            probe.put()

app = webapp2.WSGIApplication([LogSenderHandler.mapping()], debug=True)
