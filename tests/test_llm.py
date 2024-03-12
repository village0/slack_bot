"""Unit tests for the llm_integration.llm module."""
import os
import unittest
from unittest.mock import patch
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import GPT4All
from tests.constants import (
    EVAL_TEMPLATE,
    SHORT_STORY,
    SHORT_STORY_SUMMARY
)
from tests.utils import get_evaluation
from llm_integration import get_llm_answer, llm_prompt


class TestLLMPrompt(unittest.TestCase):
    """Test case class for the llm_integration.llm module.

    This class contains unit tests for the get_llm_answer and llm_prompt function in the 
    llm_integration.llm module. 
    """
    def setUp(self):
        # eval_bot_template = """
        # You are smart AI assistant that helps evaluate responses
        # from a bot to user messages.

        # User message: {user_message}
        # Bot response: {bot_response}

        # Does the bot response sufficiently answer the message by the user?
        # Only answer in "yes" or "no".
        # """

        eval_bot_template = EVAL_TEMPLATE
        # setting up llm for helping us evaluate model response
        llm = GPT4All(model=os.getenv('MODEL_PATH'), backend="gptj")
        prompt = PromptTemplate(
            template=eval_bot_template,
            input_variables=["user_message", "bot_response", "ideal_response"]
        )
        # llm_chain
        self.testing_assistant = LLMChain(prompt=prompt, llm=llm)

    def test_get_llm_answer_clean_text(self):
        """Test the get_llm_answer function with cleaned text."""
        question = 'How are you? :smiley:'
        expected_clean_text = 'How are you? '
        with patch('llm_integration.llm.llm_prompt') as mock_llm_prompt:
            mock_llm_prompt.return_value = "Response"
            get_llm_answer(question)
            mock_llm_prompt.assert_called_once_with(question=expected_clean_text)

    def test_get_llm_answer_clean_text_quotes(self):
        """Test the get_llm_answer function cleans text containing double quotes."""
        question = 'How are you? "Fine," said the AI.'
        expected_clean_text = 'How are you? <Fine,> said the AI.'
        with patch('llm_integration.llm.llm_prompt') as mock_llm_prompt:
            mock_llm_prompt.return_value = "Response"
            get_llm_answer(question)
            mock_llm_prompt.assert_called_once_with(question=expected_clean_text)

    def test_get_llm_answer_clean_text_slack_markup(self):
        """Test the get_llm_answer function removes Slack-specific markup."""
        question = 'How are you? <http://example.com/image.jpg|image>'
        expected_clean_text = 'How are you? '
        with patch('llm_integration.llm.llm_prompt') as mock_llm_prompt:
            mock_llm_prompt.return_value = "Response"
            get_llm_answer(question)
            mock_llm_prompt.assert_called_once_with(question=expected_clean_text)

    def test_get_llm_answer_all(self):
        """Test the get_llm_answer function removes Slack-specific markup, links,
        and doube quotes."""
        question = 'How are you? <http://example.com/image.jpg|image>, hehe :smiley:, "I am good".'
        expected_clean_text = 'How are you? , hehe , <I am good>.'
        with patch('llm_integration.llm.llm_prompt') as mock_llm_prompt:
            mock_llm_prompt.return_value = "Response"
            get_llm_answer(question)
            mock_llm_prompt.assert_called_once_with(question=expected_clean_text)

    def test_llm_prompt_question(self):
        """Test llm_prompt function with a general question."""
        # Input message by user
        user_message = "How are you?"
        ideal_response = "I am doing well, how can I help you today?"
        # Call the llm_prompt function
        bot_response = llm_prompt(user_message)
        # get the result, is the answer correct, yes or no
        evaluation = get_evaluation(
            self.testing_assistant,
            user_message,
            bot_response,
            ideal_response
        )
        # Assert that the response sufficiently answers the user message
        self.assertEqual(evaluation, "yes")

    def test_llm_prompt_summary(self):
        """Test llm_prompt function with a generating a summary."""
        # Input message by user
        user_message = f"Please summarize the following text: {SHORT_STORY}"
        ideal_response = SHORT_STORY_SUMMARY
        # Call the llm_prompt function
        bot_response = llm_prompt(user_message)
        # get the result, is the answer correct, yes or no
        evaluation = get_evaluation(
            self.testing_assistant,
            user_message,
            bot_response,
            ideal_response
        )
        # Assert that the response sufficiently answers the user message
        self.assertEqual(evaluation, "yes")
