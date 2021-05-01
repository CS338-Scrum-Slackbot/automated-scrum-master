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
					"text": "Story description",
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
					"text": "Select something here",
					"emoji": True
				},
				"options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "user",
                                    "emoji": True
                                },
                                "value": "field-1"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "id",
                                    "emoji": True
                                },
                                "value": "field-2"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "customer",
                                    "emoji": True
                                },
                                "value": "field-3"
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
					"text": "Select something here",
					"emoji": True
				},
				"options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Product Backlog",
                                    "emoji": True
                                },
                                "value": "swimlane-1"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Sprint Backlog",
                                    "emoji": True
                                },
                                "value": "swimlane-2"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Current Sprint",
                                    "emoji": True
                                },
                                "value": "swimlane-3"
                            }
                        ],
				"action_id": "multi_static_select-action"
			}
		}

	]
}