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
python3 src/slack_interface.py
```

You must also set up a .env file in the root directory with the parameters

```
BOT_TOKEN=your slack app bot token
SIGNING_SECRET=your slack app signing secret
```

Both of these parameters can be found on the Slack API portal

For the bot to respond to events in a slack channel (e.g. @bot), you must set up a local ngrok server which can be done by following this tutorial:

https://www.youtube.com/watch?v=6gHvqXrfjuo

Finally run:

```
./ngrok http 5000
```

And copy the forwarding address.


## Enable Events Subscription and Interactivity

To make sure your app is capturing all events, go to Events Subscriptions tab. Take the forwarding address from ngrok and paste

```
http://forwarding_address/slack/events
```

in Request URL, confirm that it is verified and click on Save Changes.

Additionally, go to Interactivity and Shortcuts tab, Take the forwarding address from ngrok and paste

```
http://forwarding_address/slack/interactive
```

in Request URL, confirm that it is verified and click on Save Changes.
