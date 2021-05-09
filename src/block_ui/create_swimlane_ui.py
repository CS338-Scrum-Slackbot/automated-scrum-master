CREATE_SWIMLANE_MODAL = {
	"type": "modal",
    "callback_id": "create-swimlane-modal",
	"title": {
		"type": "plain_text",
		"text": "Create swimlane",
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
					"text": "Autopopulated text indicating the current swimlanes",
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
					"text": "New swimlane name",
					"emoji": True
				}
        }
	]
}