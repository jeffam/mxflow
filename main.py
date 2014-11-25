#!/usr/bin/env python
#
# Copyright 2014 FreeThought Design.
#
# Licensed under the MIT license.
#
import webapp2, mxflow
from datetime import datetime, timedelta
from google.appengine.api import mail, app_identity
from models import *

# Handle requests to the main page.
class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('MXFLOW v%s' % mxflow.getVersion() + '\n')
        self.response.write('mxflow@%s.appspotmail.com' % app_identity.get_application_id() + '\n\n')

        qry = Probe.query(Probe.time_sent > datetime.now() - timedelta(days=1)).order(-Probe.time_sent)
        for probe in qry.fetch():
            self.response.write('%s: %s ' % (probe.time_sent.strftime('%c'), probe.name))
            # self.response.write(probe.time_sent)
            # self.response.write(probe.time_rec)
            if (probe.status == 1):
                self.response.write('Response in %d second(s)' % (probe.time_rec - probe.time_sent).total_seconds())
            elif (probe.status == 0):
                self.response.write('Timed out')
            else:
                self.response.write('Pending')

            self.response.write('\n')

# Handle requests to send out test emails.
class ProbeSendHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        config = mxflow.getConfig()

        # Loop through the servers to test.
        for server_name in config:
            self.response.write(server_name)

            # Create a new probe for each server.
            probe = Probe(name=server_name)
            probe_key = probe.put()

            # Send the probe email.
            self.response.write('mxflow@%s.appspotmail.com' % app_identity.get_application_id() + '\n\n')
            mail.send_mail(sender='donotreply@%s.appspotmail.com' % app_identity.get_application_id(),
              to=config[server_name]['mail'],
              subject=probe_key.urlsafe(),
              body='This is a test mxflow message.')

# Handle requests to check for probe timeouts.
class ProbeCheckHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        config = mxflow.getConfig()
        qry = Probe.query(Probe.status == -1)

        for probe in qry.fetch():
            timeout = timedelta(minutes=int(config[probe.name]['timeout']))

            if (datetime.now() > (probe.time_sent + timeout)):
                probe.status = 0
                probe.put()

                # Send out an alert mail.
                mail.send_mail(sender='donotreply@%s.appspotmail.com' % app_identity.get_application_id(),
                  to=config[probe.name]['alert'].replace('mailto:', ''),
                  subject='MXflow Alert for %s' % probe.name,
                  body='%s appears to be down. No response from test mail sent at %s.' % (probe.name, probe.time_sent))

app = webapp2.WSGIApplication([
    (r'/', MainHandler),
    (r'/probesend', ProbeSendHandler),
    (r'/probecheck', ProbeCheckHandler)
], debug=True)
