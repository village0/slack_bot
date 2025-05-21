import logging
import re
from datetime import datetime, timedelta

from slack_integration.utils import create_response_blocks, get_ai_response, get_ai_summary


async def askai(ack, command, client):
    """Takes in a question and returns a response from the AI. This is the handler for the ASK_AI_COMMAND slash command"""
    ack()
    question = command["text"]

    if not question:
        try:
            await client.async_chat_postEphemeral(
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
        await client.async_chat_postEphemeral(
            channel=command["channel_id"],
            user=command["user_id"],
            text=ack_response,
        )
    except Exception as e:
        logging.exception(f"Error sending ack ephemeral message. Error: {e}")

    # get ai response
    ai_response = await get_ai_response(question)

    if not ai_response:
        ai_response = """
        Could not generate a response, please try again later, or rephrase your question.
        """

    try:
        await client.async_chat_postEphemeral(
            channel=command["channel_id"],
            user=command["user_id"],
            text=ai_response,
            blocks=create_response_blocks(question, ai_response, is_ephemeral=True),
        )
    except Exception as e:
        logging.exception(f"Error sending ephemeral message. Error: {e}")


async def summarize_channel_messages(ack, command, client, logger):
    """Handles the /summarize slash command to summarize channel messages within a given timeframe."""
    ack()

    text = command.get("text", "").strip()
    channel_id = command.get("channel_id")
    user_id = command.get("user_id")

    time_delta = None
    unit = None

    if not text:
        error_message = "Please provide a timeframe, e.g., '2 hours', '30 minutes', or '7 days'."
    else:
        match = re.match(r"(\d+)\s+(hours|hour|h|days|day|d|minutes|minute|min|m)", text, re.IGNORECASE)
        if match:
            value = int(match.group(1))
            unit = match.group(2).lower()

            if unit in ["hours", "hour", "h"]:
                time_delta = timedelta(hours=value)
            elif unit in ["days", "day", "d"]:
                time_delta = timedelta(days=value)
            elif unit in ["minutes", "minute", "min", "m"]:
                time_delta = timedelta(minutes=value)
        else:
            error_message = "Invalid timeframe format. Please use formats like '2 hours', '30 minutes', or '7 days'."

    if time_delta:
        start_timestamp = datetime.now() - time_delta
        start_timestamp_dt = datetime.now() - time_delta
        logger.info(
            f"Summarize command called in channel {channel_id} by user {user_id} for messages since {start_timestamp_dt} ({text})"
        )
        start_timestamp_unix_string = str(start_timestamp_dt.timestamp())

        try:
            response = await client.async_conversations_history(
                channel=channel_id,
                oldest=start_timestamp_unix_string,
                inclusive=True,
                limit=1000  # Max limit per page
            )
            messages = response.get('messages', [])

            if messages:
                logger.info(f"Fetched {len(messages)} messages from channel {channel_id} since {start_timestamp_dt}")

                # Filter messages to include only those with 'text' and 'user' fields,
                # and sort them chronologically (API returns newest first, so reverse).
                # Messages without a 'user' are typically bot messages or system messages.
                # Messages without 'text' (e.g. file shares with no comment) are not useful for text summary.
                user_messages = [msg for msg in messages if 'text' in msg and 'user' in msg]
                
                # Sort by timestamp (ts string, can be compared lexicographically for chronological order)
                # Since API returns newest first, we reverse to get oldest first.
                sorted_messages = sorted(user_messages, key=lambda x: x['ts'])

                if not sorted_messages:
                    await client.async_chat_postEphemeral(
                        channel=channel_id,
                        user=user_id,
                        text="No user messages with text content found in the specified timeframe to summarize.",
                    )
                else:
                    # Concatenate message texts, prefixing with user ID for context
                    concatenated_text = "\n".join([f"U{msg['user']}: {msg['text']}" for msg in sorted_messages])

                    if not concatenated_text.strip():
                        await client.async_chat_postEphemeral(
                            channel=channel_id,
                            user=user_id,
                            text="No text content found in messages from the specified timeframe to summarize.",
                        )
                    else:
                        logger.info(f"Concatenated text length for summarization: {len(concatenated_text)}")
                        await client.async_chat_postEphemeral(
                            channel=channel_id,
                            user=user_id,
                            text=f"Generating summary for {len(sorted_messages)} processed messages...",
                        )
                        try:
                            ai_summary = await get_ai_summary(text_to_summarize=concatenated_text)

                            if ai_summary and ai_summary.strip():
                                logger.info(f"AI Summary received (first 100 chars): {ai_summary[:100]}")
                                await client.async_chat_postEphemeral(
                                    channel=channel_id,
                                    user=user_id,
                                    text=f"Here's the summary:\n{ai_summary}",
                                )
                            else:
                                logger.warning(f"AI returned an empty summary for channel {channel_id} with input length {len(concatenated_text)}.")
                                await client.async_chat_postEphemeral(
                                    channel=channel_id,
                                    user=user_id,
                                    text="The AI could not generate a summary for the given messages. Please try a different timeframe or channel.",
                                )
                        except Exception as e:
                            logger.error(f"Error getting summary from LLM for channel {channel_id}: {e}")
                            await client.async_chat_postEphemeral(
                                channel=channel_id,
                                user=user_id,
                                text="An error occurred while trying to generate the summary. Please try again.",
                            )
            else:
                await client.async_chat_postEphemeral(
                    channel=channel_id,
                    user=user_id,
                    text="No messages found in the specified timeframe.",
                )
        except Exception as e:
            logger.error(f"Error fetching messages from channel {channel_id}: {e}")
            await client.async_chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text="Sorry, there was an error fetching messages from the channel. Please try again later.",
            )
    else:
        # This part handles the case where time_delta was not successfully parsed
        # (i.e., error_message was set in the previous logic)
        try:
            await client.async_chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text=error_message,
            )
        except Exception as e:
            logger.error(f"Error sending ephemeral error message: {e}")
