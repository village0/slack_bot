import os

from dotenv import load_dotenv
from slack_bolt import App
import logging

from slack_integration.constants import (
    ASK_AI_COMMAND,
    BAD_RESPONSE,
    GOOD_RESPONSE,
    REGENERATE_RESPONSE_EPHEMERAL,
)
from slack_integration.slash_commands import (
    askai,
)

from slack_integration.actions import (
    regenerate_response_ephemeral,
    good_response,
    bad_response,
)

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()

# Initialize the Bolt app with the token and signing secret
app = App(token=os.getenv("SLACK_APP_TOKEN"))

# Bind the event handler to the app
app.command(ASK_AI_COMMAND)(askai)
app.action(REGENERATE_RESPONSE_EPHEMERAL)(regenerate_response_ephemeral)
app.action(GOOD_RESPONSE)(good_response)
app.action(BAD_RESPONSE)(bad_response)
