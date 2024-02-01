import os
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_integration.slack_app import app

if __name__ == "__main__":
    SocketModeHandler(app, os.getenv("SLACK_OAUTH_TOKEN")).start()
