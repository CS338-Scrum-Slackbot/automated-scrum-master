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
				"action_id": "plain_text_input-action",
				"placeholder": {
					"type": "plain_text",
					"text": "Hours"
				},
                "initial_value": "0"
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
					"text": "I want to..."
				},
                "initial_value": "0"
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
					"emoji": True
				},
                "initial_user": "0",
				"action_id": "users_select-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Assigned To",
				"emoji": True
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