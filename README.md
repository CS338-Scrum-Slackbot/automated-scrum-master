# Automating the Scrum Master

## How to run the bot

Git clone the repository and `cd` into it\
Run the following in the command line:
```
source .venv/slackbot/bin/activate
```

```
pip3 install -r requirements.txt
```

```
python3 slack_interface.py
```

You must also set up a .env file in the root directory with the parameters \
```
BOT_TOKEN=<your slack app bot token>
SIGNING_SECRET=<your slack app signing secret>
```

Both of these parameters can be found on the Slack API portal

For the bot to respond to events in a slack channel (e.g. @bot), you must set up a local ngrok server which can be done by following this tutorial:

https://www.youtube.com/watch?v=6gHvqXrfjuo
