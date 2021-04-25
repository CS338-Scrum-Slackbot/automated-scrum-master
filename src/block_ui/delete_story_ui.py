DELETE_STORY_MODAL = {
    "title": {
        "type": "plain_text",
        "text": "Delete a Story"
    },
    "submit": {
        "type": "plain_text",
        "text": "Submit"
    },
    "type": "modal",
    "callback_id": "delete-story-modal",
    "close": {
        "type": "plain_text",
        "text": "Cancel"
    },
    "blocks": [
        {
            "type": "input",
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
                            "value": "board-1"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Sprint Backlog",
                                "emoji": True
                            },
                            "value": "board-2"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Current Sprint",
                                "emoji": True
                            },
                            "value": "board-3"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Previous Sprints",
                                "emoji": True
                            },
                            "value": "board-4"
                        }
                        ],
                "action_id": "static_select-action"
            },
            "label": {
                "type": "plain_text",
                "text": "Pick a swimlane to delete stories from",
                "emoji": True
            }
        }
    ]
}
