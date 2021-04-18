"""
Handles interaction with Slack
"""

import slack
import os
import json
from pathlib import Path 
from dotenv import load_dotenv
from flask import Flask, request
from slackeventsapi import SlackEventAdapter

from scrum_master import ScrumMaster

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

# Signing secret is on the Slack API
slack_event_adapter = SlackEventAdapter(os.environ.get('SIGNING_SECRET'),'/slack/events', app)

client = slack.WebClient(token=os.environ.get('BOT_TOKEN'))
BOT_ID = client.api_call("auth.test")["user_id"]
CHANNEL = "#app_mention"

# Class to handle bot logic
scrum_master = ScrumMaster()

def send_message(text_msg, interactive_msg=None):
    """ Sends a message to the slack channel """
    client.chat_postMessage(channel=CHANNEL, text=text_msg, blocks=interactive_msg)

def send_modal(trigger_id, modal):
    client.views_open(trigger_id=trigger_id, view=modal) 

@app.route('/slack/interactive', methods=['POST'])
def handle_interaction():
    data = json.loads(request.form["payload"])
    if data['type'] == 'block_actions':
        try:
            if data['message']['blocks'][0]['elements'][0]['action_id'] == 'create-story':
                send_modal(data['trigger_id'], modal=scrum_master.create_story_modal())
        except KeyError:
            print("Unexpected payload. Doing nothing...")
    elif data['type'] == 'view_submission':
        scrum_master.process_story_submission(data)
    else:
        print("Unknown interactive request.")
    return ''

@slack_event_adapter.on('app_mention')
def get_app_mention(payload):
    event = payload.get('event', {})
    channel_id = event['channel']
    user_id = event['user']
    text = event['text'].split(f'<@{BOT_ID}>')[1]

    if BOT_ID != user_id:
        scrum_master.process_text(text)
        # Potentially more scrum bot logic to follow here
        text_msg, interactive_msg = scrum_master.get_response()
        send_message(text_msg, interactive_msg)

if __name__ == '__main__':
    app.run(debug=True)