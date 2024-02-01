from slack_integration.constants import (
    BAD_RESPONSE,
    GOOD_RESPONSE,
    REGENERATE_RESPONSE_EPHEMERAL,
    REGENERATE_RESPONSE_MESSAGE,
)


def get_ai_response(question):
    """Generate a response from the AI."""
    return f"This is the response from AI {question}"


def create_button_block(text, action_id, value):
    """Create a button block for a Slack message."""
    return {
        "type": "button",
        "text": {"type": "plain_text", "text": text},
        "action_id": action_id,
        "value": value if value else action_id,
    }


def create_response_blocks(question, ai_response, is_ephemeral=False):
    """Create the blocks for a Slack message."""

    return [
        {"type": "section", "text": {"type": "mrkdwn", "text": ai_response}},
        {"type": "divider"},
        {
            "type": "actions",
            "elements": [
                create_button_block(
                    "Regenerate",
                    REGENERATE_RESPONSE_EPHEMERAL
                    if is_ephemeral
                    else REGENERATE_RESPONSE_MESSAGE,
                    question,
                ),
                create_button_block("Good", GOOD_RESPONSE, ai_response),
                create_button_block("Bad", BAD_RESPONSE, ai_response),
            ],
        },
    ]
