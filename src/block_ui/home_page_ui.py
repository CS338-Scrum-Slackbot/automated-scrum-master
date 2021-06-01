INIT_HOME_PAGE = [
		{
			"type": "section",
			"block_id": "swimlane_select",
			"text": {
				"type": "mrkdwn",
				"text": "Select the swimlane you'd like to view."
			},
			"accessory": {
				"type": "radio_buttons",
				"options": [],
				"action_id": "swimlane_select"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "divider"
		},
		{
			"type": "actions",
			"block_id": "create-story-button",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Create New Story",
						"emoji": True
					},
					"value": "click_me_123",
					"action_id": "create-story"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Create New Swimlane",
						"emoji": True
					},
					"value": "click_me_123",
					"action_id": "create-swimlane"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Update Swimlane",
						"emoji": True
					},
					"value": "click_me_123",
					"action_id": "update-swimlane"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Delete Swimlane",
						"emoji": True
					},
					"value": "click_me_123",
					"action_id": "delete-swimlane"
				}
			]
		}
	]

SWIMLANE_HEADER = [
	{
		"type": "header",
		"text": {
			"type": "plain_text",
			"text": "Product Backlog",
			"emoji": True
		}
	}
]

SWIMLANE_FOOTER = [
	{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "/ Product Backlog",
					"emoji": True
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "divider"
		}
]

STORY_BLOCK = [
	{
			"type": "section",
			"fields": []
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"style": "primary",
					"text": {
						"type": "plain_text",
						"text": "Update"
					},
					"value": "update-story"
				},
				{
					"type": "button",
					"style": "danger",
					"text": {
						"type": "plain_text",
						"text": "Delete"
					},
					"value": "delete-story"
				}
			]
		},
		{
			"type": "divider"
		}
]

SORT_DROPDOWN = [
	{
			"type": "actions",
			"block_id": "sort_by",
			"elements": [
				{
					"type": "static_select",
					"placeholder": {
						"type": "plain_text",
						"text": "Sort by",
						"emoji": True
					},
					"options": [
						{
							"text": {
								"type": "plain_text",
								"text": "Priority",
								"emoji": True
							},
							"value": "priority"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Estimate",
								"emoji": True
							},
							"value": "estimate"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Status",
								"emoji": True
							},
							"value": "status"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Assigned to",
								"emoji": True
							},
							"value": "assigned_to"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "User type",
								"emoji": True
							},
							"value": "user_type"
						}
					],
					"action_id": "sort_by"
				}
			]
		}
]

SPRINT_HEADER = [
	{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Sprint 2",
				"emoji": True
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "mrkdwn",
					"text": "*Started:*"
				},
				{
					"type": "mrkdwn",
					"text": "*Ends:*"
				}
			]
		},
		{
			"type": "divider"
		}
]

RADIO_INIT_OPTION =  {
						"value": "",
						"text": {
							"type": "plain_text",
							"text": ""
						}
					}

SWIMLANE_OPTION = {
					"text": {
						"type": "plain_text",
						"text": "",
						"emoji": True
					},
					"value": ""
				}


# {"story": {"id": 13, "priority": 2, "estimate": 1, "sprint": 1, "status": "in-progress", "assigned_to": "U01TK108J86", "user_type": "Test", "story": "Test test test"}, "log": "Product Backlog", "swimlane": "Product Backlog", "sort_by": "UNSORTED"}