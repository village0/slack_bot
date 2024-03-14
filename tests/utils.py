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

    # If the option is A, B, or C answer in "yes" else "no".
    if "A" in evaluation_text  or "B" in evaluation_text  or "C" in evaluation_text:
        return True
    return False
