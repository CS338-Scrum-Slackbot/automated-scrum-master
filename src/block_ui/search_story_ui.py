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
			"type": "input",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Product Backlog",
                                    "emoji": True
                                },
                                "value": "board-1"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Sprint Backlog",
                                    "emoji": True
                                },
                                "value": "board-2"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Current Sprint",
                                    "emoji": True
                                },
                                "value": "board-3"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Previous Sprints",
                                    "emoji": True
                                },
                                "value": "board-4"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Archived",
                                    "emoji": True
                                },
                                "value": "board-5"
                            }
                        ],
				"action_id": "static_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Swimlane (optional)",
				"emoji": True
			}
		},


		{
			"type": "input",
			"element": {
				"type": "static_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an item",
					"emoji": True
				},
				"options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Product Backlog",
                                    "emoji": True
                                },
                                "value": "board-1"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Sprint Backlog",
                                    "emoji": True
                                },
                                "value": "board-2"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Current Sprint",
                                    "emoji": True
                                },
                                "value": "board-3"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Previous Sprints",
                                    "emoji": True
                                },
                                "value": "board-4"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Archived",
                                    "emoji": True
                                },
                                "value": "board-5"
                            }
                        ],
				"action_id": "static_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Swimlane (optional)",
				"emoji": True
			}
		},


		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "third block"
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
                                "value": "board-1"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Sprint Backlog",
                                    "emoji": True
                                },
                                "value": "board-2"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Current Sprint",
                                    "emoji": True
                                },
                                "value": "board-3"
                            }
                        ],
				"action_id": "multi_static_select-block-three"
			}
		}

	]
}