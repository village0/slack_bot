"""Utils file for tests, contains helper functions"""

def get_evaluation(testing_assistant, user_message, bot_response, ideal_response):
    """
    Returns evaluation based on grading rubric.
    All grades above D are for acceptable answers.
    """
    evaluation_response = testing_assistant.invoke({
        "user_message": user_message,
        "bot_response": bot_response,
        "ideal_response": ideal_response
    })
    evaluation_text = evaluation_response["text"]
    print("Evaluation AI Generated Response:", evaluation_text)

    valid_options = ["A", "B", "C"]

    # If the option is A, B, or C, test passes
    if any(x in evaluation_text for x in valid_options):
        return True
    return False
