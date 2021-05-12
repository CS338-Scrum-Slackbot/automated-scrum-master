HOME_PAGE_BLOCK = [
		{
			"type": "section",
			"block_id": "swimlane_select",
			"text": {
				"type": "mrkdwn",
				"text": "Select the swimlanes you'd like to see."
			},
			"accessory": {
				"type": "radio_buttons",
				"options": [
					{
						"text": {
							"type": "plain_text",
							"text": "Product Backlog",
							"emoji": True
						},
						"value": "value-0"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Sprint Backlog",
							"emoji": True
						},
						"value": "value-1"
					},
					{
						"text": {
							"type": "plain_text",
							"text": "Current Sprint",
							"emoji": True
						},
						"value": "value-2"
					}
				],
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
				}
			]
		},
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Product Backlog",
				"emoji": True
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Search",
						"emoji": True
					},
					"value": "click_me_123",
					"action_id": "actionId-0"
				},
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
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Estimate",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Status",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Assigned to",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "User type",
								"emoji": True
							},
							"value": "value-2"
						}
					],
					"action_id": "actionId-4"
				}
			]
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Priority*: High"
				},
				{
					"type": "mrkdwn",
					"text": "*Estimate*: 3"
				},
				{
					"type": "mrkdwn",
					"text": "*Assigned to*: Nathan"
				},
				{
					"type": "mrkdwn",
					"text": "*Status*: To-do"
				},
				{
					"type": "mrkdwn",
					"text": "*User Type*: Customer"
				},
				{
					"type": "mrkdwn",
					"text": "*Story*: As a customer, I want to have a home page."
				},
				{
					"type": "mrkdwn",
					"text": "*Description*: This story describes the idea that our app should have a home page."
				}
			]
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
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Priority*"
				},
				{
					"type": "mrkdwn",
					"text": "*Type*"
				},
				{
					"type": "plain_text",
					"text": "High"
				},
				{
					"type": "plain_text",
					"text": "String"
				}
			]
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
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "/Product Backlog",
					"emoji": True
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "divider"
		},
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": "Sprint Backlog",
				"emoji": True
			}
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Search",
						"emoji": True
					},
					"value": "click_me_123",
					"action_id": "actionId-0"
				},
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
							"value": "value-0"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Estimate",
								"emoji": True
							},
							"value": "value-1"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Status",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "Assigned to",
								"emoji": True
							},
							"value": "value-2"
						},
						{
							"text": {
								"type": "plain_text",
								"text": "User type",
								"emoji": True
							},
							"value": "value-2"
						}
					],
					"action_id": "actionId-4"
				}
			]
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Priority*"
				},
				{
					"type": "mrkdwn",
					"text": "*Type*"
				},
				{
					"type": "plain_text",
					"text": "High"
				},
				{
					"type": "plain_text",
					"text": "String"
				}
			]
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
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Priority*"
				},
				{
					"type": "mrkdwn",
					"text": "*Type*"
				},
				{
					"type": "plain_text",
					"text": "High"
				},
				{
					"type": "plain_text",
					"text": "String"
				}
			]
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
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "/Sprint Backlog",
					"emoji": True
				}
			]
		}
	]