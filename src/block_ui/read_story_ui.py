READ_STORY_BLOCK = {
    # Not sure if this needs a callback ID.
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Status: - \t ID: - \t Sprint: -"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "My story text here\nMore story text"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Assigned to: - \nPriority: - \nEstimate: -\nSwimlane: -"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Edit",
						"emoji": true
					},
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Move",
						"emoji": true
					},
					"value": "click_me_123"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Delete",
						"emoji": true
					},
					"value": "click_me_123"
				}
			]
		}
	]
}