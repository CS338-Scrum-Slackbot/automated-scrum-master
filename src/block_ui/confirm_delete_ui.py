CONFIRM_DELETE_MODAL = {
    "response_action": "update",
    "view": {
        "type": "modal",
        "title": {
            "type": "plain_text",
            "text": "Confirm Delete"
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "text": "Are you sure you want to delete?",
                    "emoji": True
                }
            }
        ]
    }
}
