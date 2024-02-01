import logging

from slack_integration.utils import create_response_blocks, get_ai_response


def askai(ack, command, client):
    """Takes in a question and returns a response from the AI. This is the handler for the ASK_AI_COMMAND slash command"""
    ack()
    question = command["text"]

    if not question:
        try:
            client.chat_postEphemeral(
                channel=command["channel_id"],
                user=command["user_id"],
                text="Please provide a question",
            )
        except Exception as e:
            logging.exception(f"Error sending ephemeral message. Error: {e}")
        return

    # send an ack for message received
    try:
        ack_response = f"Generating response to your question: {question}"
        client.chat_postEphemeral(
            channel=command["channel_id"],
            user=command["user_id"],
            text=ack_response,
        )
    except Exception as e:
        logging.exception(f"Error sending ack ephemeral message. Error: {e}")

    # get ai response
    ai_response = get_ai_response(question)

    try:
        client.chat_postEphemeral(
            channel=command["channel_id"],
            user=command["user_id"],
            text=ai_response,
            blocks=create_response_blocks(question, ai_response, is_ephemeral=True),
        )
    except Exception as e:
        logging.exception(f"Error sending ephemeral message. Error: {e}")
