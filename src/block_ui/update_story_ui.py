UPDATE_STORY_MODAL = {
	"title": {
		"type": "plain_text",
		"text": "Update Story"
	},
	"submit": {
		"type": "plain_text",
		"text": "Submit"
	},
	"blocks": [
		{
			"type": "input",
			"label": {
				"type": "plain_text",
				"text": "Swimlane",
				"emoji": True
			},
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
						"value": "product_backlog"
					}
				],
				"initial_option": {
					"text": {
						"type": "plain_text",
						"text": "Product Backlog",
						"emoji": True
					},
					"value": "product_backlog"
				},
				"action_id": "static_select-action"
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"multiline": True,
				"action_id": "plain_text_input-action",
				"placeholder": {
					"type": "plain_text",
					"text": "As a ___, I want to..."
				},
                "initial_value": "0"
			},
			"label": {
				"type": "plain_text",
				"text": "Story Title"
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_text_input-action",
				"placeholder": {
					"type": "plain_text",
					"text": "End user, administrator, etc."
				},
                "initial_value": "0"
			},
			"label": {
				"type": "plain_text",
				"text": "User Type"
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "plain_text_input-action",
				"placeholder": {
					"type": "plain_text",
					"text": "Sprint number"
				},
                "initial_value": "1"
			},
			"label": {
				"type": "plain_text",
				"text": "Sprint"
			},
			"hint": {
				"type": "plain_text",
				"text": "Must be an integer."
			}
		},
		{
			"type": "input",
			"element": {
				"type": "users_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select users",
					"emoji": True
				},
                "initial_user": "None",
				"action_id": "users_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Assigned To",
				"emoji": True
			},
			"hint": {
				"type": "plain_text",
				"text": "Select a user to assign this story to or leave blank if unassigned."
			}
		},
		{
			"type": "input",
			"element": {
				"type": "radio_buttons",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "None",
							"emoji": True
						},
						"value": "none"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "To-do",
							"emoji": True
						},
						"value": "to-do"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "In-progress",
							"emoji": True
						},
						"value": "in-progress"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Completed",
							"emoji": True
						},
						"value": "completed"
					}
				],
                "initial_option": {
					"text": {
						"type": "plain_text",
						"text": "None",
						"emoji": True
					},
					"value": "none"
				},
				"action_id": "radio_buttons-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Status",
				"emoji": True
			}
		},
		{
			"type": "input",
			"element": {
				"type": "radio_buttons",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "High",
							"emoji": True
						},
						"value": "high"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Medium",
							"emoji": True
						},
						"value": "medium"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Low",
							"emoji": True
						},
						"value": "low"
					}
				],
                "initial_option": {
					"text": {
						"type": "plain_text",
						"text": "Low",
						"emoji": True
					},
					"value": "low"
				},
				"action_id": "radio_buttons-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Priority",
				"emoji": True
			}
		},
		{
			"type": "input",
			"element": {
				"type": "static_select",
				"action_id": "plain_text_input-action",
				"placeholder": {
					"type": "plain_text",
					"text": "Select an estimate"
				},
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "1",
							"emoji": True
						},
						"value": "1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "2",
							"emoji": True
						},
						"value": "2"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "3",
							"emoji": True
						},
						"value": "3"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "5",
							"emoji": True
						},
						"value": "5"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "8",
							"emoji": True
						},
						"value": "8"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "13",
							"emoji": True
						},
						"value": "13"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "21",
							"emoji": True
						},
						"value": "21"
					}
				],
				"initial_option": {
					"text": {
						"type": "plain_text",
						"text": "1",
						"emoji": True
					},
					"value": "1"
				},
				"action_id": "static_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Estimate",
				"emoji": True
			},
		},
	],
	"type": "modal",
    "callback_id": "update-story-modal",
	"private_metadata": "0",
}