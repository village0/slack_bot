import logging

from slack_integration.constants import (
    BAD_RESPONSE,
    GOOD_RESPONSE,
    REGENERATE_RESPONSE_EPHEMERAL,
    REGENERATE_RESPONSE_MESSAGE,
)
from llm_integration.llm import get_llm_answer


def get_ai_response(question):
    """Returns a response from the LLM."""
    print("I am here")
    return get_llm_answer(question)


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


def send_slack_message(client, channel, text, blocks=None, metadata=None):
    try:
        return client.chat_postMessage(
            channel=channel,
            text=text,
            blocks=blocks,
            metadata={"event_type": "direct_message", "event_payload": metadata},
        )
    except Exception as e:
        logging.exception(f"Error sending message: {e}")


def update_slack_message(client, channel, ts, text, blocks=None, metadata=None):
    try:
        client.chat_update(
            channel=channel,
            ts=ts,
            text=text,
            blocks=blocks,
            metadata={"event_type": "direct_message", "event_payload": metadata},
        )
    except Exception as e:
        logging.exception(f"Error updating message: {e}")
