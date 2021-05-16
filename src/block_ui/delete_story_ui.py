DELETE_STORY_MODAL = {
    "title": {
        "type": "plain_text",
        "text": "Delete Story"
    },
    "type": "modal",
    "callback_id": "delete-story-modal",
    "blocks": [
        {
            "type": "divider"
        },
        {
            "dispatch_action": True,
            "type": "input",
            "element": {
                    "type": "plain_text_input",
                    "action_id": "confirm-delete"
            },
            "label": {
                "type": "plain_text",
                "text": "Enter comma-seperated list of ids for the stories you want to delete",
                "emoji": True
            }
        }
    ]
}
