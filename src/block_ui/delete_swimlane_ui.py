DELETE_SWIMLANE_MODAL = {
	"type": "modal",
    "callback_id": "delete-swimlane-modal",
	"title": {
		"type": "plain_text",
		"text": "Delete swimlane",
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
                    "text": "Any stories in a deleted swimlane will be moved to `archived `. You cannot delete default swimlanes.",
                }
		},
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
                    "text": "Select from these swimlanes",
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
                    }
                ],
                "action_id": "static_select-action"
            }
        }

	]
}