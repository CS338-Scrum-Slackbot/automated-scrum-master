READ_STORY_BLOCK = [
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": ""
				}
			]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Edit"
					},
					"value": "edit-story"
				},
				{
					"type": "button",
					"style": "primary",
					"text": {
						"type": "plain_text",
						"text": "Move"
					},
					"value": "move-story"
				},
				{
					"type": "button",
					"style": "danger",
					"text": {
						"type": "plain_text",
						"text": "Delete"
					},
					"value": "delete-story"
				}
			]
		}
]