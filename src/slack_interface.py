"""
Handles interaction with Slack
"""

from sys import call_tracing
from scrum_master import ScrumMaster
from slackeventsapi import SlackEventAdapter
from flask import Flask, request
import json
from dotenv import load_dotenv
from pathlib import Path
import slack
import os
import time
from datetime import datetime

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

# Signing secret is on the Slack API
slack_event_adapter = SlackEventAdapter(
    os.environ.get('SIGNING_SECRET'), '/slack/events', app)

client = slack.WebClient(token=os.environ.get('BOT_TOKEN'))
BOT_ID = client.api_call("auth.test")["user_id"]

# TODO: Change CHANNEL when developing locally"
CHANNEL = "#nathan"

# delete all scheduled messages on start-up
result = client.chat_scheduledMessages_list()
for msg in result["scheduled_messages"]:
    print(msg['id'])
    try:
        result = client.chat_deleteScheduledMessage(
            channel=CHANNEL,
            scheduled_message_id=msg['id']
        )
    except:
        pass


# Class to handle bot logic
scrum_master = ScrumMaster()
SCRUM_BOARD = 'data/scrum_board.json'
view_actions = ['update-story', 'delete-story',
                'create-story', 'update-swimlane', 'create-swimlane']

# reset sprint info in json:
scrum_master.reset_sprint_info()


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
    id_to_name = {x['id']: x['real_name']
                  for x in members if not x['is_bot'] and x['real_name'] != 'Slackbot'}
    with open(file=SCRUM_BOARD, mode="r+") as f:
        js = json.load(f)
        js['metadata']['id_to_name'] = id_to_name
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

        # result = client.chat_scheduledMessages_list()
        # for msg in result["scheduled_messages"]:
        #     print(msg)

        if 'view' in data:
            # print('\n\nVIEW CHANGED\n\n')
            if data['view']['type'] == 'home':
                if data['actions'][0]['action_id'] in view_actions:
                    action_id = data['actions'][0]['action_id']
                    value = data['actions'][0]['value']
                    send_modal(data['trigger_id'], modal=scrum_master.create_modal(
                        action_id, metadata=value))
                else:
                    updateHome(data, init=0)
        else:
            try:
                # Get the action_id and value fields from the event payload
                action_id = data['actions'][0]['action_id']
                value = data['actions'][0]['value']
            except KeyError as e:
                print("Unexpected payload. Doing nothing...")
                return ''
            # Send a modal with our obtained trigger_id
            # Which modal to send is evaluated in scrum_master based on the provided action_id
            if action_id == 'end-sprint':
                end_sprint()
                text_msg, interactive_msg = scrum_master.get_response()
                send_message(text_msg, interactive_msg)
            elif action_id == 'extend-sprint':
                extend_sprint()
                text_msg, interactive_msg = scrum_master.get_response()
                send_message(text_msg, interactive_msg)
            else:
                send_modal(data['trigger_id'], modal=scrum_master.create_modal(
                    action_id, metadata=value))

    # A view submission payload is received when a user submits a modal
    elif data['type'] == 'view_submission':
        try:
            callback_id = data['view']['callback_id']
            # print(f'\n\nVIEW SUBMISSION METADATA: {data["view"]["private_metadata"]}\n\n')
            if callback_id == "start-sprint-modal":
                print("START SPRINT MODAL SUBMITTED")
                schedule_sprint_end_message(
                    list(data['view']['state']['values'].values()))
            # Extract relevant data from modal
            response = scrum_master.process_modal_submission(
                data, callback_id)

            # Get text and block response from backend
            text_msg, interactive_msg = scrum_master.get_response()
            # if swimlane updated, need to update swimlane in private_metadata
            # IF it's the current selection
            if response:
                try:
                    md = json.loads(data['view']['private_metadata'])
                    # has_metadata = True
                    if md['swimlane'] == response[0]:  # old name
                        # "Product Backlog" #response[1]
                        md['swimlane'] = response[1]
                        md['old_swimlane'] = response[0]
                        data['view']['private_metadata'] = json.dumps(md)
                    # print(f'\n\nMETADATA IN UPDATE\n\n')
                    # print(json.dumps(data, indent=4))
                    for b in data['view']['blocks'][1]['element']['options']:
                        if b['text']['text'] == response[0]:
                            # "Product Backlog"#
                            b['text']['text'] = response[1]
                            b['value'] = response[1]  # "Product Backlog" #
                except:
                    data['view']['private_metadata'] = json.dumps(
                        {'swimlane': response[1], 'old_swimlane': response[0]})  # "Product Backlog"})#response[1]})

                    # print(f'\n\nNO METADATA IN UPDATE\n\n')
                    # print(json.dumps(data, indent=4))

            # Send message to slack channel
            send_message(text_msg, interactive_msg)
            updateHome(data, init=0, after_button=True)

        except KeyError as e:
            if e == 'callback_id':
                print("YOU MUST INCLUDE A callback_id FIELD IN YOUR MODAL!!")
    else:
        print("Unknown interactive request.")
    return ''


def end_sprint():
    # schedule a new end message
    sprint_end = scrum_master.scrum_board.read_metadata_field(
        'current_sprint_ends')
    sprint_duration = scrum_master.scrum_board.read_metadata_field(
        'sprint_duration')

    new_end = sprint_end + sprint_duration
    end_msg = scrum_master.get_sprint_end_msg(sprint_end, new_end)
    # delete old message if necessary:
    old_msg_id = scrum_master.get_end_sprint_msg_id()
    delete_scheduled_message(old_msg_id)
    success = schedule_message(new_end, blocks=end_msg['blocks'])
    # call scrum_master.end_sprint()
    scrum_master.end_sprint(button=True, success=success)


def extend_sprint():
    # NOTE: extends sprint by 1 day
    # schedule a new end message
    day = 300  # 86400
    sprint_start = scrum_master.scrum_board.read_metadata_field(
        'current_sprint_starts')
    sprint_end = scrum_master.scrum_board.read_metadata_field(
        'current_sprint_ends')
    new_end = sprint_end + day

    end_msg = scrum_master.get_sprint_end_msg(sprint_start, new_end)
    # delete old message if necessary:
    old_msg_id = scrum_master.get_end_sprint_msg_id()
    delete_scheduled_message(old_msg_id)
    success = schedule_message(new_end, blocks=end_msg['blocks'])
    if success:
        scrum_master.save_sched_message(
            'end_sprint', success["scheduled_message_id"])
    scrum_master.extend_sprint(new_end=new_end, success=success)


def schedule_sprint_end_message(payload_values):
    # print(json.dumps(payload_values, indent=4))
    start_date = payload_values[0]['sprint-date']['selected_date']
    start_time = payload_values[0]['sprint-time']['selected_time']
    duration = int(payload_values[1]['duration']
                   ['selected_option']['text']['text'])
    unit = payload_values[1]['unit']['selected_option']['text']['text']
    seconds_table = {
        'days': 86400,
        'weeks': 604800,
        'months': 2419200,
    }
    duration_in_seconds = 300  # duration * seconds_table[unit]
    unix_start = int(datetime.strptime(
        f'{start_date} {start_time}', '%Y-%m-%d %H:%M').timestamp())
    unix_end = unix_start + duration_in_seconds

    print(f'SPRINT STARTS: {unix_start} AND ENDS {unix_end}')

    # Q022FRWA1GT

    # if already have an end_sprint msg scheduled, need to delete it:
    exists = scrum_master.check_if_sprint_exists()
    if exists:
        print("SPRINT EXISTS ALREADY")
        delete_scheduled_message(exists)
    else:
        print("SPRINT DOESN'T EXIST")

    # schedule a message:
    print("GETTING END MESSAGE")
    end_msg = scrum_master.get_sprint_end_msg(unix_start, unix_end)
    print("SCHEDULING MESSAGE")
    success = schedule_message(unix_end, blocks=end_msg['blocks'])
    print("HANDLING SPRINT SUBMISSION")
    scrum_master.handle_sprint_submission(
        unix_start, unix_end, success=success)


def delete_scheduled_message(message_id):
    try:
        result = client.chat_deleteScheduledMessage(
            channel=CHANNEL,
            scheduled_message_id=message_id
        )
        return result['ok']
    except:
        return 0


def schedule_message(time, text="", blocks=[]):
    try:
        result = client.chat_scheduleMessage(
            channel=CHANNEL,
            text=text,
            blocks=blocks,
            post_at=time
        )
        return result

    except:
        # print("Error scheduling message: {}".format(e))
        return None
        # logger.error("Error scheduling message: {}".format(e))


@slack_event_adapter.on('team_join')
def team_join_event(payload):
    # print('TEAM JOIN DETECTED!!')
    register_or_update_member(payload)
    return ''


@slack_event_adapter.on('user_change')
def user_change_event(payload):
    # print('USER CHANGE DETECTED!!')
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
    # print(f'\n\n\nDISPLAY HOME EVENT\n\n\n')
    updateHome(payload, init=not 'view' in payload)


def updateHome(payload, init, after_button=False):
    button_metadata = None
    # time.sleep(1)
    if after_button:
        # print('\n\nAFTER BUTTON\n\n')
        # print(json.dumps(payload, indent=4), "\n\n")
        button_metadata = payload['view']['private_metadata']
    if init:
        user_id = payload.get("event", {}).get("user")
        md = json.loads(payload['event']['view']['private_metadata'])
        sw = scrum_master.scrum_board.list_user_swimlanes()
        if md['swimlane'] in sw:
            md['swimlane'] = "Product Backlog"
        payload['event']['view']['private_metadata'] = json.dumps(md)
        view = scrum_master.update_home(
            payload['event'], metadata=payload['event']['view']['private_metadata'])
    else:
        user_id = payload['user']['id']
        view = scrum_master.update_home(payload, metadata=button_metadata)

    # print(json.dumps(view, indent=4))
    client.views_publish(user_id=user_id, view=view)
    # view = scrum_master.update_home(payload['event'], metadata=payload['event']['view']['private_metadata'])
    # client.views_publish(user_id=user_id, view=view)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
