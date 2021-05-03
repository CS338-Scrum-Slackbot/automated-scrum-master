CREATE_STORY_MODAL = {
            "type": "modal",
            "callback_id": "create-story-modal",
            "title": {
                "type": "plain_text",
                "text": "Create a Story",
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
                        "text": "Fill out the following to create a story",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "label": {
                        "type": "plain_text",
                        "text": "Swim Lane",
                        "emoji": True
                    },
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
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Archived",
                                    "emoji": True
                                },
                                "value": "board-5"
                            }
                        ],
                        "action_id": "static_select-action"
                    }
                },
                {
                    "type": "input",
                    "label": {
                        "type": "plain_text",
                        "text": "Priority",
                        "emoji": True
                    },
                    "element": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select an number",
                            "emoji": True
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Low",
                                    "emoji": True
                                },
                                "value": "priority-1"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "Medium",
                                    "emoji": True
                                },
                                "value": "priority-2"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "High",
                                    "emoji": True
                                },
                                "value": "priority-3"
                            }
                        ],
                        "action_id": "static_select-action"
                    }
                },
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
                                    "text": "1",
                                    "emoji": True
                                },
                                "value": "estimate-1"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "2",
                                    "emoji": True
                                },
                                "value": "estimate-2"
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "3",
                                    "emoji": True
                                },
                                "value": "estimate-3"
                            }
                        ],
                        "action_id": "static_select-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Estimate",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Sprint",
                        "emoji": True
                    }
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Assigned to"
                    },
                    "accessory": {
                        "type": "users_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select a user",
                            "emoji": True
                        },
                        "action_id": "users_select-action"
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "plain_text_input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "User type",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "plain_text_input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Story description",
                        "emoji": True
                    }
                }
            ],
}