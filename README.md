# mxflow

![mxflow logo](mxflow-logo.png "mxflow") Simple round-trip email monitoring

## About

mxflow is a free mail server monitor that periodically sends email messages
to a test mailbox on your server. If that message isn't delivered back
within a configurable amount of time, you'll receive an alert.

mxflow runs on [App Engine](https://cloud.google.com/appengine/docs) and can
be run for free without billing enabled, when using the default settings and
monitoring a single server.

## Setup

1. Create a new App Engine project. Note the *Project ID* (AKA *App ID*).
2. Download a copy of this application.
3. Adjust the settings:
    - In app.yaml, set `application: <your app id>`
    - Create a file called `config.ini` and add one or more servers to monitor.
      See `example.config.ini` for more info.
    - Optionally adjust the settings in `cron.yaml`. Note that the default
      values are set to keep the application under the billing limits. If you
      increase the `/probesend` task to a level where it sends more than 100
      messages a day, you'll hit the free quota and the probes will stop
      working. Also note that alert emails count toward the quota. See the
      [mail quota info](https://cloud.google.com/appengine/docs/quotas#Mail) for
      details.
4. Add a mailbox _on your mail server_ and configure it to forward mail to the
    [receiving email](https://cloud.google.com/appengine/docs/python/mail/receivingmail)
    for your App Engine instance. The receiving email looks like this:
    *string*@*appid*.appspotmail.com
5. Deploy the application to App Engine. This is left as an exercise for the
    reader, although I'm sure that a tutorial would be welcome.

## Changelog

### v1.0.0 - 2014-11-25

- Initial version

## Contributing

Pull requests for fixes and new features are welcome. This is my first
useful Python application, so feel free to set me straight where necessary!

### Plans/Ideas

- Fix time displays to use local time zone
- Add a new cron task (and setting?) to truncate the probe history
- Add charts showing round-trip performance over time
- Save the server configuration in the datastore and allow it to be modified
  without re-deploying the app
