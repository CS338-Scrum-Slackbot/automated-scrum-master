SEARCH_STORY_MODAL = {
	"type": "modal",
    "callback_id": "search-story-modal",
	"title": {
		"type": "plain_text",
		"text": "Search story",
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit",
	},
	"blocks": [
		{
			"type": "section",
			"text": 
				{
					"type": "plain_text",
					"text": "Fill out the following to search for a story",
				}
		},
		{
				"type": "input",
				"element": {
					"type": "plain_text_input",
					"multiline": False,
					"action_id": "plain_text_input-action"
				},
				"label": {
					"type": "plain_text",
					"text": "Search text",
					"emoji": True
				}
        },
		

		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Field (optional)"
			},
			"accessory": {
				"type": "multi_static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select fields",
					"emoji": True
				},
				"options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Default field",
                                    "emoji": True
                                },
                                "value": "field-1"
                            }
                        ],
				"action_id": "multi_static_select-action"
			}
		},


	{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Swimlane (optional)"
			},
			"accessory": {
				"type": "multi_static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select swimlanes",
					"emoji": True
				},
				"options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Default swimlane",
                                    "emoji": True
                                },
                                "value": "swimlane-1"
                            }
                        ],
				"action_id": "multi_static_select-action"
			}
		}

	]
}