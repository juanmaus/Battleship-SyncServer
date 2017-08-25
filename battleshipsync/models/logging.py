#!/usr/bin/python
# -*- coding: utf-8 -*-
from mongoengine import *
import datetime
import uuid


# ---------------------------------------------------------------------------------------
# CLASS LOG ENTRY
# ---------------------------------------------------------------------------------------
class LogEntry(Document):

    """
        Represents a log entry that can be stored inside a Mongo Database in order
        to keep track of events and actions done by players. 
    """

    # Define entity attributes

    who = StringField(max_length=150, required=False)
    entry_id = StringField(max_length=40, required=True, default=str(uuid.uuid4()))
    logger = StringField(max_length=500, required=False)
    level = StringField(max_length=500, required=False)
    trace = StringField(max_length=4000, required=False)
    message = StringField(max_length=4096, required=True)
    path = StringField(max_length=500, required=False)
    method = StringField(max_length=100, required=False)
    ip = StringField(max_length=20, required=False)
    created = DateTimeField(default=datetime.datetime.now)

    meta = {
        'indexes': [
            'entry_id',
            'level',
            'ip'
        ]
    }

    # -----------------------------------------------------------------------------------
    # METHOD TO SLACK MSG
    # -----------------------------------------------------------------------------------
    def to_slack_msg(self):
        """
            Gets a string representation of the log entry created when an event happens.
            This entry is used to be passed as payload when sending events to slack
            channel. 
            :return: string with the message that will be displayed on Slack.
        """
        msg = 'Level: [' + self.level + '] \n'
        msg += 'IP Address: [' + self.ip + '] \n'
        msg += 'Message: [' + self.message + '] \n'
        return msg
