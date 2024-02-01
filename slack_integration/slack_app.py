import os

from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import logging

from constants import (
    ASK_AI_COMMAND,
    BAD_RESPONSE,
    GOOD_RESPONSE,
    REGENERATE_RESPONSE_EPHEMERAL,
)
from slash_commands import (
    askai,
)

from actions import (
    regenerate_response_ephemeral,
    good_response,
    bad_response,
)

# Initialize logging
logging.basicConfig(level=logging.DEBUG)

# Load environment variables
load_dotenv()

# Initialize the Bolt app with the token and signing secret
app = App(token=os.getenv("SLACK_BOT_TOKEN"))

# Bind the event handler to the app
app.command(ASK_AI_COMMAND)(askai)
app.action(REGENERATE_RESPONSE_EPHEMERAL)(regenerate_response_ephemeral)
app.action(GOOD_RESPONSE)(good_response)
app.action(BAD_RESPONSE)(bad_response)


if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()
