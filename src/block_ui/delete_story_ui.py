DELETE_STORY_MODAL = {
    "title": {
        "type": "plain_text",
        "text": "Delete Story"
    },
    "type": "modal",
    "submit": {
        "type": "plain_text",
        "text": "Submit",
    },
    "callback_id": "delete-story-modal",
    "blocks": [
        {
            "type": "divider"
        },
        {
            "type": "input",
            "element": {
                    "type": "plain_text_input",
                    "action_id": "plain_text_input-action"
            },
            "label": {
                "type": "plain_text",
                "text": "Enter comma-seperated list of ids for the stories you want to delete",
                "emoji": True
            }
        }
    ]
}
