import os
REGENERATE_RESPONSE_EPHEMERAL = "regenerateResponseEphemeral"
REGENERATE_RESPONSE_MESSAGE = "regenerateResponseMessage"
GOOD_RESPONSE = "goodResponse"
BAD_RESPONSE = "badResponse"
ASK_AI_COMMAND = f"/{os.getenv('SLACK_SLASH_COMMAND', 'askai')}"
INBOX_MESSAGE_EVENT = "message"
