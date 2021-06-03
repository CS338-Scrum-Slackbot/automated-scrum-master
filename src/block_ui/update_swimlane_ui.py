UPDATE_SWIMLANE_MODAL = {
    "type": "modal",
    "callback_id": "update-swimlane-modal",
    "title": {
            "type": "plain_text",
        "text": "Update swimlane",
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
                    "text": "You cannot update default swimlanes.",
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

UPDATE_NO_SWIMLANES_MODAL = {
    "type": "modal",
    "title": {
            "type": "plain_text",
        "text": "Update Swimlane",
                "emoji": True
    },
    "close": {
        "type": "plain_text",
        "text": "Close",
        "emoji": True
    },
    "blocks": [
        {
            "type": "section",
            "text": {
                    "type": "plain_text",
                    "text": "No swimlanes can be updated.",
                    "emoji": True
            }
        }
    ]
}
