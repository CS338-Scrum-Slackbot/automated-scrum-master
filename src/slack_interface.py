"""
Handles interaction with Slack
"""

from scrum_master import ScrumMaster
from slackeventsapi import SlackEventAdapter
from flask import Flask, request
import json
from dotenv import load_dotenv
import json_reader
from pathlib import Path
import slack
import os

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

# Signing secret is on the Slack API
slack_event_adapter = SlackEventAdapter(
    os.environ.get('SIGNING_SECRET'), '/slack/events', app)

client = slack.WebClient(token=os.environ.get('BOT_TOKEN'))
BOT_ID = client.api_call("auth.test")["user_id"]

# TODO: Change CHANNEL when developing locally"
CHANNEL = "#app_mention"

# Class to handle bot logic
scrum_master = ScrumMaster()
SCRUM_BOARD = 'data/scrum_board.json'

def get_member(id):
    try: 
        ret = client.users_info(user=id)['user']['profile']
    except:
        ret = None
    return ret

def get_all_members():
    return client.api_call(api_method="users.list")['members']

def populate_members():
    members = get_all_members()
    # print(json.dumps(members, indent=4))
    id_to_name = {x['id']:x['real_name'] for x in members if not x['is_bot'] and x['real_name'] != 'Slackbot'}
    with open(file=SCRUM_BOARD, mode="r+") as f:
        js = json.load(f)
        js['metadata']['id_to_name'] =  id_to_name
        f.seek(0)
        f.write(json.dumps(js, indent=4))
        f.truncate()

populate_members()

def send_message(text_msg, interactive_msg=None):
    """ Sends a message to the slack channel

        Keyword Args:
        text_msg -- The textual content of the message you want to send
        interactive_msg -- The interactive component of the message (e.g. buttons, checkboxes, etc)
    """
    client.chat_postMessage(
        channel=CHANNEL, text=text_msg, blocks=interactive_msg)


def send_modal(trigger_id, modal):
    """Sends a modal into the slack channel

        Keyword Args:
        trigger_id -- An id used to initiate interactive communication (e.g. modals) between the user and bot.
                      We obtain the trigger_id when the user clicks the button that creates the modal.
        modal -- The JSON object of the modal we want sent to the channel
    """
    client.views_open(trigger_id=trigger_id, view=modal)

def register_or_update_member(payload):
    event = payload.get("event", {})
    user_id = event.get("user", {}).get("id")
    real_name = event.get("user", {}).get("real_name")
    with open(file=SCRUM_BOARD, mode="r+") as f:
        js = json.load(f)
        js['metadata']['id_to_name'][user_id] = real_name
        f.seek(0)
        f.write(json.dumps(js, indent=4))
        f.truncate()

@app.route('/slack/interactive', methods=['POST'])
def handle_interaction():
    data = json.loads(request.form["payload"])

    # A data type of block_actions is received when a user clicks on an interactive block in the channel
    if data['type'] == 'block_actions':
        try:
            # Get the action_id and value fields from the event payload
            action_id = data['actions'][0]['action_id']
            value = data['actions'][0]['value']
        except KeyError as e:
            print("Unexpected payload. Doing nothing...")
            return ''
        # Send a modal with our obtained trigger_id
        # Which modal to send is evaluated in scrum_master based on the provided action_id
        send_modal(data['trigger_id'], modal=scrum_master.create_modal(action_id, metadata=value))

    # A view submission payload is received when a user submits a modal
    elif data['type'] == 'view_submission':
        try:
            callback_id = data['view']['callback_id']

            # Extract relevant data from modal
            scrum_master.process_modal_submission(
                data, callback_id)
            
            # Get text and block response from backend
            text_msg, interactive_msg = scrum_master.get_response()

            # Send message to slack channel
            send_message(text_msg, interactive_msg)

        except KeyError as e:
            if e=='callback_id':
                print("YOU MUST INCLUDE A callback_id FIELD IN YOUR MODAL!!")
    else:
        print("Unknown interactive request.")
    return ''

@slack_event_adapter.on('team_join')
def team_join_event(payload):
    print('TEAM JOIN DETECTED!!')
    register_or_update_member(payload)
    return ''

@slack_event_adapter.on('user_change')
def user_change_event(payload):
    print('USER CHANGE DETECTED!!')
    register_or_update_member(payload)
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
        scrum_master.reset()

@slack_event_adapter.on('app_home_opened')
def displayHome(payload):
    print('\n\nAPP HOME OPENED\n\n')
    print(json.dumps(payload, indent=4))
    user_id = payload.get("event", {}).get("user")
    print(f'\n\nUSER ID: {user_id}')
    view = scrum_master.update_home()
    client.views_publish(user_id=user_id, view=view)

def updateHome(user):
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
