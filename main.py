import os
import pyperclip
import requests
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

# Load environment variables
load_dotenv(dotenv_path=".env.sample")

# Initialize the Bolt app with the token and signing secret
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

# Define action IDs as constants
REGENERATE_RESPONSE = "regenerateResponse"
COPY_TEXT = "copyText"
GOOD_RESPONSE = "goodResponse"
BAD_RESPONSE = "badResponse"


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


def create_blocks(question, ai_response):
    """Create the blocks for a Slack message."""
    return [
        {"type": "section", "text": {"type": "mrkdwn", "text": ai_response}},
        {"type": "divider"},
        {
            "type": "actions",
            "elements": [
                create_button_block("Regenerate", REGENERATE_RESPONSE, question),
                create_button_block("Copy", COPY_TEXT, ai_response),
                create_button_block("Good", GOOD_RESPONSE, ai_response),
                create_button_block("Bad", BAD_RESPONSE, ai_response),
            ],
        },
    ]


@app.command("/askai")
def askai(ack, command, client):
    """Handle the /askai command."""
    ack()
    question = command["text"]

    if not question:
        client.chat_postEphemeral(
            channel=command["channel_id"],
            user=command["user_id"],
            text="Please provide a question",
        )
        return

    ai_response = get_ai_response(question)
    client.chat_postEphemeral(
        channel=command["channel_id"],
        user=command["user_id"],
        text=ai_response,
        blocks=create_blocks(question, ai_response),
    )


@app.action(REGENERATE_RESPONSE)
def regenerate(ack, body):
    """Handle the regenerateResponse action."""
    ack()

    question = body["actions"][0]["value"]
    ai_response = get_ai_response(question)

    requests.post(
        body["response_url"],
        json={
            "replace_original": True,
            "text": ai_response,
            "blocks": create_blocks(question, ai_response),
        },
    )


@app.action(COPY_TEXT)
def copyText(ack, body):
    """Handle the copyText action."""
    ack()
    ai_response = body["actions"][0]["value"]
    pyperclip.copy(ai_response)


@app.action(GOOD_RESPONSE)
def goodResponse(ack, body):
    """Handle the goodResponse action."""
    ack()


@app.action(BAD_RESPONSE)
def badResponse(ack, body):
    """Handle the badResponse action."""
    ack()


if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
