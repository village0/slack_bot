"""Unit tests for the llm_integration.llm module."""
import unittest
from unittest.mock import patch
from llm_integration import get_llm_answer


class TestLLMPrompt(unittest.TestCase):
    """Test case class for the llm_integration.llm module.

    This class contains unit tests for the get_llm_answer and llm_prompt function in the 
    llm_integration.llm module. 
    """
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
