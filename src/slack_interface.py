"""
Handles interaction with Slack
"""

import slack
import os
from pathlib import Path 
from dotenv import load_dotenv
from flask import Flask 
from slackeventsapi import SlackEventAdapter

from scrum_master import ScrumMaster

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

# Signing secret is on the Slack API
slack_event_adapter = SlackEventAdapter(os.environ['SIGNING_SECRET'],'/slack/events', app)

client = slack.WebClient(token=os.environ['BOT_TOKEN'])
BOT_ID = client.api_call("auth.test")["user_id"]
CHANNEL = "#test"

# Class to handle bot logic
scrum_master = ScrumMaster()

def send_message(msg):
    """ Sends a message to the slack channel """
    client.chat_postMessage(channel=CHANNEL, text=msg)

@slack_event_adapter.on('app_mention')
def get_app_mention(payload):
    event = payload.get('event', {})
    channel_id = event['channel']
    user_id = event['user']
    text = event['text'].split(f'<@{BOT_ID}> ')[1]

    if BOT_ID != user_id:
        scrum_master.process_text(text)
        # Potentially more scrum bot logic to follow here
        response = scrum_master.get_response()
        send_message(response)

if __name__ == '__main__':
    app.run(debug=True)