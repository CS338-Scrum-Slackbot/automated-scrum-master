SPRINT_END_MSG = {
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Sprint 2 has ended!",
				"emoji": True
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "*Started:* 5/10/2021 at 9:00"
				},
				{
					"type": "mrkdwn",
					"text": "*Ended:* 5/17/2021 at 9:00"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Please choose how you would like to proceed. You *must* select an option below to ensure your sprint cycle continues."
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Extend Sprint",
						"emoji": True
					},
					"value": "click_me_123",
					"action_id": "extend-sprint"
				},
				{
					"type": "button",
					"style": "danger",
					"text": {
						"type": "plain_text",
						"text": "End Current Sprint & Start New Sprint",
						"emoji": True
					},
					"value": "click_me_123",
					"action_id": "end-sprint"
				}
			]
		}
	]
}
