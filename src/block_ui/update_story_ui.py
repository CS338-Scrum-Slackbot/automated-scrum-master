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
			"element": {
				"type": "plain_text_input",
				"action_id": "sl_input",
				"placeholder": {
					"type": "plain_text",
					"text": "Hours"
				}
			},
			"label": {
				"type": "plain_text",
				"text": "Estimate"
			},
			"hint": {
				"type": "plain_text",
				"text": "Number of hours the task will take."
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
							"emoji": true
						},
						"value": "high"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Medium",
							"emoji": true
						},
						"value": "medium"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Low",
							"emoji": true
						},
						"value": "low"
					}
				],
				"action_id": "radio_buttons-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Priority",
				"emoji": true
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
							"emoji": true
						},
						"value": "none"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "To-do",
							"emoji": true
						},
						"value": "to-do"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "In-progress",
							"emoji": true
						},
						"value": "in-progress"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Completed",
							"emoji": true
						},
						"value": "completed"
					}
				],
				"action_id": "radio_buttons-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Status",
				"emoji": true
			}
		},
		{
			"type": "input",
			"element": {
				"type": "plain_text_input",
				"action_id": "sl_input",
				"placeholder": {
					"type": "plain_text",
					"text": "End user, administrator, etc."
				}
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
				"action_id": "sl_input",
				"placeholder": {
					"type": "plain_text",
					"text": "I want to..."
				}
			},
			"label": {
				"type": "plain_text",
				"text": "User Story"
			}
		},
		{
			"type": "input",
			"element": {
				"type": "users_select",
				"placeholder": {
					"type": "plain_text",
					"text": "Select users",
					"emoji": true
				},
				"action_id": "users_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Assigned To",
				"emoji": true
			},
			"hint": {
				"type": "plain_text",
				"text": "Select a user to assign this story to."
			}
		}
	],
	"type": "modal",
    "callback_id": "update-story-modal",
}

# "initial_option": {
#     "text": {
#         "type": "plain_text",
#         "text": "Completed",
#         "emoji": true
#     },
#     "value": "value-3"
# },