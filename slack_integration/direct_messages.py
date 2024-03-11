from slack_integration.utils import (
    create_response_blocks,
    get_ai_response,
    send_slack_message,
    update_slack_message,
)


def handle_direct_message(client, event):
    """Handle a direct message event."""
    print(event)
    question = event["text"]

    if not question:
        send_slack_message(client, event["channel"], "Please provide a question")
        return

    # Send an ack for message received
    ack_response = f"Generating response to your question: {question}"
    loading_message = send_slack_message(client, event["channel"], ack_response)

    # Get AI response
    ai_response = get_ai_response(question)

    if not ai_response:
        ai_response = """
        Could not generate a response, please try again later, or rephrase your question.
        """

    if loading_message is None:
        send_slack_message(
            client,
            event["channel"],
            ai_response,
            create_response_blocks(question, ai_response),
            metadata=event,
        )
    else:
        update_slack_message(
            client,
            event["channel"],
            loading_message["ts"],
            ai_response,
            create_response_blocks(question, ai_response),
            metadata=event,
        )
