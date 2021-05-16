CONFIRM_DELETE_MODAL = {
    "title": {
        "type": "plain_text",
        "text": "Confirm Delete"
    },
    "submit": {
        "type": "plain_text",
        "text": "Submit"
    },
    "type": "modal",
    "callback_id": "confirm-delete-modal",
    "close": {
        "type": "plain_text",
        "text": "Cancel"
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
