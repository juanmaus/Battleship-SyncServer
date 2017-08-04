from flask import request
from battleshipsync.models.logging import LogEntry
import json
import requests
import logging
import traceback


class SlackWebhookClient:
    # --------------------------------------------------------------------------
    # CONSTRUCTOR METHOD
    # --------------------------------------------------------------------------
    def __init__(self, webhook):
        self.webhook = webhook

    # --------------------------------------------------------------------------
    # METHOD SEND
    # --------------------------------------------------------------------------
    def send(self, message, emoji, username):
        payload = {
            "username": username,
            "icon_emoji": emoji,
            "text": message
        }
        json_payload = json.dumps(payload)
        resp = requests.post(self.webhook, data=json_payload)
        return resp.status_code


# ------------------------------------------------------------------------------
# CLASS SLACK LOG HANDLER
# ------------------------------------------------------------------------------
class SlackLogHandler(logging.Handler):

    # --------------------------------------------------------------------------
    # METHOD SET WEBHOOK
    # --------------------------------------------------------------------------
    def set_webhook(self, webhook):
        """
            Sets the URI of the webhook where events are going to be sent using http
            POST.
            :param webhook: The URI of the webhook
            :return: nothing
        """
        self.webhook = webhook
        return

    # --------------------------------------------------------------------------
    # METHOD EMIT
    # --------------------------------------------------------------------------
    def emit(self, record):

        """
            Implements the actual logic of persisting and sending an event to Slack's
            webhooks.
            :param record: The log event data
            :return: nothing
        """

        trace = None
        exc = record.__dict__['exc_info']
        if exc:
            trace = traceback.format_exc(exc)
        path = request.path
        method = request.method
        ip = request.remote_addr
        slack_event = LogEntry(
            logger=record.__dict__['name'],
            level=record.__dict__['levelname'],
            trace=trace,
            message=record.__dict__['msg'],
            path=path,
            method=method,
            ip=ip,
        )
        slack_event.save()
        hook = SlackWebhookClient(self.webhook)
        hook.send(
            message=slack_event.to_slack_msg(),
            emoji=":ghost:",
            username="battleship-server"
        )

