"""Unit tests for the llm_integration.llm module."""
import os
import unittest
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import GPT4All
from tests.constants import (
    EVAL_TEMPLATE,
    SHORT_STORY,
    SHORT_STORY_SUMMARY,
    TEXT,
    REPHRASED_TEXT,
    INFORMAL_EMAIL,
    FORMAL_EMAIL,
    EXPLANATION,
    IDEATION
)
from tests.utils import get_evaluation
from slack_integration import get_ai_response


class TestSlackUtils(unittest.TestCase):
    """Test case class for the slack_integration.utils module.

    This class contains unit tests for the get_ai_response function in the slack_integration.utils
    module. 
    """
    def setUp(self):
        """Initialize new llm for testing responses by slack bot llm"""
        eval_bot_template = EVAL_TEMPLATE
        # setting up llm for helping us evaluate model response
        llm = GPT4All(model=os.getenv('MODEL_PATH'), backend="gptj")
        prompt = PromptTemplate(
            template=eval_bot_template,
            input_variables=["user_message", "bot_response", "ideal_response"]
        )
        # llm_chain
        self.testing_assistant = LLMChain(prompt=prompt, llm=llm)

    def test_llm_prompt_question(self):
        """Test llm_prompt function with a general question."""
        # Input message by user
        user_message = "How are you?"
        ideal_response = "I am doing well, how can I help you today?"
        # Call the llm_prompt function
        bot_response = get_ai_response(user_message)
        # get the result, is the answer correct, yes or no
        evaluation = get_evaluation(
            self.testing_assistant,
            user_message,
            bot_response,
            ideal_response
        )
        # Assert that the response sufficiently answers the user message
        self.assertTrue(evaluation)

    def test_llm_prompt_summary(self):
        """Test llm_prompt function with generating a summary."""
        # Input message by user
        user_message = f"Please summarize the following text: {SHORT_STORY}"
        ideal_response = SHORT_STORY_SUMMARY
        # Call the llm_prompt function
        bot_response = get_ai_response(user_message)
        # get the result, is the answer correct, yes or no
        evaluation = get_evaluation(
            self.testing_assistant,
            user_message,
            bot_response,
            ideal_response
        )
        # Assert that the response sufficiently answers the user message
        self.assertTrue(evaluation)

    def test_llm_prompt_rephrase(self):
        """Test llm_prompt function with rephrasing a text."""
        # Input message by user
        user_message = f"Please rephrase this text to be clearer: {TEXT}"
        ideal_response = REPHRASED_TEXT
        # Call the llm_prompt function
        bot_response = get_ai_response(user_message)
        # get the result, is the answer correct, yes or no
        evaluation = get_evaluation(
            self.testing_assistant,
            user_message,
            bot_response,
            ideal_response
        )
        # Assert that the response sufficiently answers the user message
        self.assertTrue(evaluation)

    def test_llm_prompt_rewrite(self):
        """Test llm_prompt function with rewriting an email."""
        # Input message by user
        user_message = f"Please rewrite this email to sound formal: {INFORMAL_EMAIL}"
        ideal_response = FORMAL_EMAIL
        # Call the llm_prompt function
        bot_response = get_ai_response(user_message)
        # get the result, is the answer correct, yes or no
        evaluation = get_evaluation(
            self.testing_assistant,
            user_message,
            bot_response,
            ideal_response
        )
        # Assert that the response sufficiently answers the user message
        self.assertTrue(evaluation)

    def test_llm_prompt_explain(self):
        """Test llm_prompt function with explaining a concept."""
        # Input message by user
        user_message = "Explain what multithreading in python is"
        ideal_response = EXPLANATION
        # Call the llm_prompt function
        bot_response = get_ai_response(user_message)
        # get the result, is the answer correct, yes or no
        evaluation = get_evaluation(
            self.testing_assistant,
            user_message,
            bot_response,
            ideal_response
        )
        # Assert that the response sufficiently answers the user message
        self.assertTrue(evaluation)

    def test_llm_prompt_ideate(self):
        """Test llm_prompt function with ideating."""
        # Input message by user
        user_message = "Ideate ways to increase productivity at work"
        ideal_response = IDEATION
        # Call the llm_prompt function
        bot_response = get_ai_response(user_message)
        # get the result, is the answer correct, yes or no
        evaluation = get_evaluation(
            self.testing_assistant,
            user_message,
            bot_response,
            ideal_response
        )
        # Assert that the response sufficiently answers the user message
        self.assertTrue(evaluation)
