# Automating the Scrum Master

## How to run the bot

1. Git clone the repository and `cd` into it. 
2. Create a python virtual environment and activate it with:
```
python3 -m venv .venv/slackbot
source .venv/slackbot/bin/activate
```
3. Install package dependencies with:
```
pip3 install -r requirements.txt
```

4. Run the bot with:
```
python3 slack_interface.py
```

You must also set up a .env file in the root directory with the parameters 
```
BOT_TOKEN=your slack app bot token
SIGNING_SECRET=your slack app signing secret
```

Both of these parameters can be found on the Slack API portal

For the bot to respond to events in a slack channel (e.g. @bot), you must set up a local ngrok server which can be done by following this tutorial:

https://www.youtube.com/watch?v=6gHvqXrfjuo
