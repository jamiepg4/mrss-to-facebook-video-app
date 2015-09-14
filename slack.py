import os
import requests


def slack_info_message(message):
    """
    Send an informational message to Slack
    """
    channel = os.getenv('SLACK_CHANNEL_SUCCESS')
    if not channel:
        return
    slack_message(channel, message)


def slack_error_message(message):
    """
    Send an error message to Slack
    """
    channel = os.getenv('SLACK_CHANNEL_ERROR')
    if not channel:
        return
    slack_message(channel, message)


def slack_message(channel, message):
    """
    Send a message to Slack
    """
    webhook_url = os.getenv('SLACK_WEBHOOK_URL')
    if not webhook_url:
        return
    body = {
        'channel': channel,
        'text': message
    }
    requests.post(webhook_url, json=body)
