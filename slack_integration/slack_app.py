import logging
import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.error import BoltUnhandledRequestError

from slack_integration.actions import (
    bad_response,
    good_response,
    regenerate_response_ephemeral,
    regenerate_response_message,
)
from slack_integration.constants import (
    ASK_AI_COMMAND,
    BAD_RESPONSE,
    GOOD_RESPONSE,
    INBOX_MESSAGE_EVENT,
    REGENERATE_RESPONSE_EPHEMERAL,
    REGENERATE_RESPONSE_MESSAGE,
)
from slack_integration.direct_messages import handle_direct_message
from slack_integration.slash_commands import askai

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()

# Initialize the Bolt app with the token and signing secret
app = App(token=os.getenv("SLACK_APP_TOKEN"))

# Bind the event handler to the app
app.command(ASK_AI_COMMAND)(askai)
app.event(INBOX_MESSAGE_EVENT)(handle_direct_message)
app.action(REGENERATE_RESPONSE_EPHEMERAL)(regenerate_response_ephemeral)
app.action(GOOD_RESPONSE)(good_response)
app.action(BAD_RESPONSE)(bad_response)
app.action(REGENERATE_RESPONSE_MESSAGE)(regenerate_response_message)


@app.error
def handle_errors(error):
    """TODO: ignore unhandled request types"""
    if isinstance(error, BoltUnhandledRequestError):
        # you may want to have some logging here
        # return BoltResponse(status=200, body="")
        pass
    else:
        # other error patterns
        # return BoltResponse(status=500, body="Something Wrong")
        pass
