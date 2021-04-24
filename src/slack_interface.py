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
    """ Sends a message to the slack channel 
        
        Keyword Args:
        text_msg -- The textual content of the message you want to send
        interactive_msg -- The interactive component of the message (e.g. buttons, checkboxes, etc)
    """
    client.chat_postMessage(channel=CHANNEL, text=text_msg, blocks=interactive_msg)

def send_modal(trigger_id, modal):
    """Sends a modal into the slack channel

        Keyword Args:
        trigger_id -- An id used to initiate interactive communication (e.g. modals) between the user and bot.
                      We obtain the trigger_id when the user clicks the button that creates the modal.
        modal -- The JSON object of the modal we want sent to the channel
    """
    client.views_open(trigger_id=trigger_id, view=modal) 

@app.route('/slack/interactive', methods=['POST'])
def handle_interaction():
    data = json.loads(request.form["payload"])

    # A data type of block_actions is received when a user clicks on an interactive block in the channel
    if data['type'] == 'block_actions':
        try:
            action_id = data['message']['blocks'][0]['elements'][0]['action_id']
        except KeyError:
            print("Unexpected payload. Doing nothing...")
            return ''

        # Send a modal with our obtained trigger_id
        # Which modal to send is evaluated in scrum_master based on the provided action_id
        send_modal(data['trigger_id'], modal=scrum_master.create_modal(action_id))
        

    # A view submission payload is received when a user submits a modal
    elif data['type'] == 'view_submission':
        try:
            callback_id = data['view']['callback_id']
            scrum_master.process_modal_submission(data, callback_id)
            text_msg, interactive_msg = scrum_master.get_response()
            send_message(text_msg, interactive_msg)
        except KeyError:
            print("YOU MUST INCLUDE A callback_id FIELD IN YOUR MODAL!!")
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
        scrum_master.process_user_msg(text)
        # Potentially more scrum bot logic to follow here
        text_msg, interactive_msg = scrum_master.get_response()
        send_message(text_msg, interactive_msg)

if __name__ == '__main__':
    app.run(debug=True)