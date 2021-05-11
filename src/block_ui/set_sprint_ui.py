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
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*When should the sprint to start?*"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "datepicker",
					"initial_date": "1990-04-28",
					"placeholder": {
						"type": "plain_text",
						"text": "Select a date",
						"emoji": True
					},
					"action_id": "actionId-0"
				},
				{
					"type": "timepicker",
					"initial_time": "13:37",
					"placeholder": {
						"type": "plain_text",
						"text": "Select time",
						"emoji": True
					},
					"action_id": "actionId-5"
				}
			]
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*How long should the sprint last?*"
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Duration",
						"emoji": True
					},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "1",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "2",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "3",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "4",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "5",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "6",
								"emoji": True
							},
							"value": "value-2"
						}
					],
					"action_id": "static_select-action"
				},
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Unit of time",
						"emoji": True
					},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "days",
								"emoji": True
							},
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "weeks",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "months",
								"emoji": True
							},
							"value": "value-2"
						}
					],
					"action_id": "static_select-action-2"
				}
			]
		}
	]
}
