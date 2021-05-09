SET_SPRINT_MODAL = {
    "title": {
        "type": "plain_text",
        "text": "Set Sprint Period"
    },
    "submit": {
        "type": "plain_text",
        "text": "Submit"
    },
    "type": "modal",
    "callback_id": "start-sprint-modal",
    "close": {
        "type": "plain_text",
        "text": "Cancel"
    },
    "blocks": [
		{
			"type": "input",
			"element": {
				"type": "datepicker",
				"initial_date": "1990-04-28",
				"placeholder": {
					"type": "plain_text",
					"text": "Select a date",
					"emoji": True
				},
				"action_id": "datepicker-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Date",
				"emoji": True
			}
		},
		{
			"type": "input",
			"element": {
				"type": "timepicker",
				"initial_time": "13:37",
				"placeholder": {
					"type": "plain_text",
					"text": "Select time",
					"emoji": True
				},
				"action_id": "timepicker-action"
			},
			"label": {
				"type": "plain_text",
				"text": "Time",
				"emoji": True
			}
		}
	]
}
