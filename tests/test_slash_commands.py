import unittest
from unittest.mock import MagicMock, AsyncMock, patch, call
import asyncio
from datetime import datetime, timedelta

from slack_integration.slash_commands import summarize_channel_messages

class TestSummarizeCommandTimeframeParsing(unittest.IsolatedAsyncioTestCase):

    async def _test_timeframe_scenario(self, input_text, expected_ephemeral_text_start_or_exact, is_exact=False):
        ack = MagicMock()
        # Patch the client's methods used before the part we're testing for timeframe parsing
        # The async_conversations_history is called if parsing succeeds.
        # We want to check the message sent if parsing fails, or the first message if it succeeds.
        client = AsyncMock()
        
        # Default behavior for successful parse leading to no messages
        # This setup is for when parsing *succeeds*
        if not is_exact: # For error messages, we expect an exact match
             client.async_conversations_history.return_value = {'messages': []}


        logger = MagicMock()
        command = {
            "text": input_text,
            "channel_id": "C123",
            "user_id": "U456"
        }

        await summarize_channel_messages(ack, command, client, logger)

        ack.assert_called_once()
        self.assertTrue(client.async_chat_postEphemeral.called)
        
        # Get the arguments of the last call to async_chat_postEphemeral for error messages
        # or the first relevant one for success cases
        # For successful parsing, the first ephemeral message might be "Generating summary..."
        # or "No messages found..." if history is empty.
        # For failed parsing, it's an error message.

        # We need to inspect the 'text' argument of the call to async_chat_postEphemeral
        # If parsing fails, this is the error message.
        # If parsing succeeds, it tries to fetch messages. If that's empty, it sends "No messages found...".
        # If messages are found and processed, it sends "Generating summary...".
        # The logic in summarize_channel_messages sends multiple ephemeral messages in success scenarios.
        # For timeframe parsing tests, we are most interested in the *first* feedback if parsing fails,
        # or the fact that it *proceeds* if parsing succeeds.

        # Let's check the text of the *last* ephemeral message for simplicity in this helper for now.
        # This means for successful parses, we check the final outcome of that branch.
        actual_text = client.async_chat_postEphemeral.call_args.kwargs['text']
            
        if is_exact:
            self.assertEqual(actual_text, expected_ephemeral_text_start_or_exact)
        else:
            # For successful parsing, it will eventually hit the "No messages found" or "Generating summary"
            # Let's assume the "No messages found..." path for successful parsing with empty history
            self.assertTrue(actual_text.startswith(expected_ephemeral_text_start_or_exact),
                            f"Expected text starting/matching '{expected_ephemeral_text_start_or_exact}', but got '{actual_text}'")

    async def test_valid_timeframe_2_hours(self):
        await self._test_timeframe_scenario("2 hours", "No messages found in the specified timeframe.")

    async def test_valid_timeframe_7_days(self):
        await self._test_timeframe_scenario("7 days", "No messages found in the specified timeframe.")

    async def test_valid_timeframe_30_minutes(self):
        await self._test_timeframe_scenario("30 minutes", "No messages found in the specified timeframe.")
    
    async def test_valid_timeframe_1h(self):
        await self._test_timeframe_scenario("1h", "No messages found in the specified timeframe.")

    async def test_valid_timeframe_3d(self):
        await self._test_timeframe_scenario("3d", "No messages found in the specified timeframe.")

    async def test_valid_timeframe_15m(self):
        await self._test_timeframe_scenario("15m", "No messages found in the specified timeframe.")

    async def test_valid_timeframe_1_hour_singular(self):
        await self._test_timeframe_scenario("1 hour", "No messages found in the specified timeframe.")

    async def test_valid_timeframe_1_day_singular(self):
        await self._test_timeframe_scenario("1 day", "No messages found in the specified timeframe.")

    async def test_valid_timeframe_1_minute_singular(self):
        await self._test_timeframe_scenario("1 minute", "No messages found in the specified timeframe.")

    async def test_invalid_timeframe_format_foo_bar(self):
        await self._test_timeframe_scenario("foo bar", "Invalid timeframe format. Please use formats like '2 hours', '30 minutes', or '7 days'.", is_exact=True)

    async def test_invalid_timeframe_empty_string(self):
        await self._test_timeframe_scenario("", "Please provide a timeframe, e.g., '2 hours', '30 minutes', or '7 days'.", is_exact=True)

    async def test_invalid_timeframe_10_weeks(self):
        await self._test_timeframe_scenario("10 weeks", "Invalid timeframe format. Please use formats like '2 hours', '30 minutes', or '7 days'.", is_exact=True)
    
    async def test_invalid_timeframe_no_number(self):
        await self._test_timeframe_scenario("hours", "Invalid timeframe format. Please use formats like '2 hours', '30 minutes', or '7 days'.", is_exact=True)

    async def test_invalid_timeframe_no_unit(self):
        await self._test_timeframe_scenario("10", "Invalid timeframe format. Please use formats like '2 hours', '30 minutes', or '7 days'.", is_exact=True)


class TestSummarizeCommandHandler(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.ack = MagicMock()
        self.command = {
            "text": "1 hour", # Valid timeframe for these tests
            "channel_id": "C123",
            "user_id": "U456"
        }
        self.client = AsyncMock()
        self.logger = MagicMock()

        # Common sample messages
        self.sample_messages = [
            {'user': 'U1', 'text': 'Hello world', 'ts': '1678886400.000001'}, # Oldest
            {'user': 'U2', 'text': 'How are you?', 'ts': '1678886401.000002'},
            {'user': 'U1', 'text': 'Good, thanks!', 'ts': '1678886402.000003'} # Newest (if API returns like this)
        ]
        # Note: summarize_channel_messages sorts these into chronological (oldest first)
        self.concatenated_sample_text = "U1: Hello world\nU2: How are you?\nU1: Good, thanks!"


    @patch('slack_integration.slash_commands.get_ai_summary', new_callable=AsyncMock)
    async def test_successful_summarization(self, mock_get_ai_summary):
        self.client.async_conversations_history.return_value = {'messages': self.sample_messages}
        mock_get_ai_summary.return_value = "This is a summary."

        await summarize_channel_messages(self.ack, self.command, self.client, self.logger)

        self.ack.assert_called_once()
        self.client.async_conversations_history.assert_called_once()
        mock_get_ai_summary.assert_called_once_with(text_to_summarize=self.concatenated_sample_text)
        
        # Check the ephemeral messages sent
        # First one is "Generating summary..."
        # Second one is the actual summary
        self.assertEqual(self.client.async_chat_postEphemeral.call_count, 2)
        calls = self.client.async_chat_postEphemeral.call_args_list
        self.assertTrue(calls[0].kwargs['text'].startswith("Generating summary for 3 processed messages..."))
        self.assertEqual(calls[1].kwargs['text'], "Here's the summary:\nThis is a summary.")

    async def test_no_messages_found_from_history(self):
        self.client.async_conversations_history.return_value = {'messages': []}

        await summarize_channel_messages(self.ack, self.command, self.client, self.logger)
        
        self.ack.assert_called_once()
        self.client.async_conversations_history.assert_called_once()
        self.client.async_chat_postEphemeral.assert_called_once_with(
            channel="C123", user="U456", text="No messages found in the specified timeframe."
        )

    async def test_no_user_text_messages_found(self):
        # Messages that will be filtered out
        filtered_messages = [
            {'ts': '1678886400.000001'}, # No user, no text
            {'user': 'U1', 'ts': '1678886401.000002'}, # No text
            {'text': 'A message', 'ts': '1678886402.000003'} # No user
        ]
        self.client.async_conversations_history.return_value = {'messages': filtered_messages}

        await summarize_channel_messages(self.ack, self.command, self.client, self.logger)

        self.ack.assert_called_once()
        self.client.async_conversations_history.assert_called_once()
        self.client.async_chat_postEphemeral.assert_called_once_with(
            channel="C123", user="U456", text="No user messages with text content found in the specified timeframe to summarize."
        )
    
    async def test_no_actual_text_content_after_processing(self):
        # Messages that have user and text, but text is only whitespace
        whitespace_messages = [
            {'user': 'U1', 'text': '   ', 'ts': '1678886400.000001'},
            {'user': 'U2', 'text': '\n \t ', 'ts': '1678886401.000002'}
        ]
        self.client.async_conversations_history.return_value = {'messages': whitespace_messages}

        await summarize_channel_messages(self.ack, self.command, self.client, self.logger)
        
        self.ack.assert_called_once()
        self.client.async_conversations_history.assert_called_once()
        self.client.async_chat_postEphemeral.assert_called_once_with(
            channel="C123", user="U456", text="No text content found in messages from the specified timeframe to summarize."
        )

    @patch('slack_integration.slash_commands.get_ai_summary', new_callable=AsyncMock)
    async def test_llm_fails_to_summarize_returns_none(self, mock_get_ai_summary):
        self.client.async_conversations_history.return_value = {'messages': self.sample_messages}
        mock_get_ai_summary.return_value = None # Simulate LLM returning None

        await summarize_channel_messages(self.ack, self.command, self.client, self.logger)

        self.ack.assert_called_once()
        mock_get_ai_summary.assert_called_once_with(text_to_summarize=self.concatenated_sample_text)
        
        # Last ephemeral message should be the error
        self.client.async_chat_postEphemeral.assert_called_with( # assert_called_with checks the last call
            channel="C123", user="U456", text="The AI could not generate a summary for the given messages. Please try a different timeframe or channel."
        )

    @patch('slack_integration.slash_commands.get_ai_summary', new_callable=AsyncMock)
    async def test_llm_call_raises_exception(self, mock_get_ai_summary):
        self.client.async_conversations_history.return_value = {'messages': self.sample_messages}
        mock_get_ai_summary.side_effect = Exception("LLM Processing Error")

        await summarize_channel_messages(self.ack, self.command, self.client, self.logger)

        self.ack.assert_called_once()
        mock_get_ai_summary.assert_called_once_with(text_to_summarize=self.concatenated_sample_text)
        self.client.async_chat_postEphemeral.assert_called_with(
            channel="C123", user="U456", text="An error occurred while trying to generate the summary. Please try again."
        )

    async def test_error_fetching_messages_api_raises_exception(self):
        self.client.async_conversations_history.side_effect = Exception("Slack API Error")

        await summarize_channel_messages(self.ack, self.command, self.client, self.logger)

        self.ack.assert_called_once()
        self.client.async_conversations_history.assert_called_once()
        self.client.async_chat_postEphemeral.assert_called_once_with(
            channel="C123", user="U456", text="Sorry, there was an error fetching messages from the channel. Please try again later."
        )


if __name__ == '__main__':
    unittest.main()
