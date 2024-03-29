import logging

import requests

from slack_integration.utils import create_response_blocks, get_ai_response


def regenerate_response_ephemeral(ack, body):
    """Handle the regenerateResponse action."""
    ack()

    question = body["actions"][0]["value"]
    if not question:
        logging.error("No question provided")
        return

    ai_response = get_ai_response(question)

    if not ai_response:
        ai_response = """
        Could not generate a response, please try again later, or rephrase your question.
        """

    try:
        requests.post(
            body["response_url"],
            json={
                "replace_original": True,
                "text": ai_response,
                "blocks": create_response_blocks(
                    question, ai_response, is_ephemeral=True
                ),
            },
        )
    except Exception as e:
        logging.exception(f"Error sending ephemeral message. Error: {e}")


def good_response(ack, body):
    """Handle the goodResponse action."""
    ack()


def bad_response(ack, body):
    """Handle the badResponse action."""
    ack()


def regenerate_response_message(ack, body):
    """Handle the regenerateResponse action."""
    ack()
    question = body["message"]["metadata"]["event_payload"]["text"]

    if not question:
        logging.error("No question provided")
        return

    ai_response = get_ai_response(question)

    if not ai_response:
        ai_response = """
        Could not generate a response, please try again later, or rephrase your question.
        """

    try:
        requests.post(
            body["response_url"],
            json={
                "replace_original": True,
                "text": ai_response,
                "blocks": create_response_blocks(question, ai_response),
                "metadata": body["message"]["metadata"],
            },
        )
    except Exception as e:
        logging.exception(f"Error sending ephemeral message. Error: {e}")
