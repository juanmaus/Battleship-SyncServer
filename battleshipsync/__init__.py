#!/usr/bin/python
# -*- coding: utf-8 -*-
import logging
from battleshipsync.extensions.slack_event_handler import SlackLogHandler
from flask import Flask
from flask_mongoengine import MongoEngine
from flask_jwt import JWT
from flask_redis import FlaskRedis

# ------------------------------------------------------------------------------
# SETUP GENERAL APPLICATION
# ------------------------------------------------------------------------------

__version__ = '1.0'
app = Flask('battleshipsync')
app.config.from_object('config')
app.debug = True

# ------------------------------------------------------------------------------
# SETUP LOGGING
# ------------------------------------------------------------------------------

# Slack/Mongo Handler
handler = SlackLogHandler()
print(app.config['SLACK_WEBHOOK'])
handler.set_webhook(app.config['SLACK_WEBHOOK'])
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)


# ------------------------------------------------------------------------------
# SETUP MONGO DB 
# ------------------------------------------------------------------------------

db = MongoEngine(app)

# ------------------------------------------------------------------------------
# SETUP REDIS
# ------------------------------------------------------------------------------

redis_store = FlaskRedis(app, strict=False)

# ------------------------------------------------------------------------------
# SETUP JWT AUTHENTICATION
# ------------------------------------------------------------------------------

# Import all battleshipsync controller files
from battleshipsync.controllers import *
from battleshipsync.security import idam

jwt = JWT(app, idam.authenticate, idam.identity)
