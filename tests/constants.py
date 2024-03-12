"""Constants for unit tests"""

EVAL_TEMPLATE = """
You are an assistant that evaluates how well the smart assistant
answers a user question by comparing the response to the ideal (expert) response
Output a single letter and nothing else.

You are comparing a submitted answer to an expert answer on a given question.
Here is the data:
    [BEGIN DATA]
    ************
    [Question]: {user_message}
    ************
    [Expert]: {ideal_response}
    ************
    [Submission]: {bot_response}
    ************
    [END DATA]

Compare the factual content of the submitted answer with the expert answer.
Ignore any differences in style, grammar, or punctuation.
The submitted answer may either be a subset or superset of the expert answer, 
or it may conflict with it. Determine which case applies. 
Answer the question by selecting one of the following options:
    (A) The submitted answer is a subset of the expert answer and is fully consistent with it.
    (B) The submitted answer is a superset of the expert answer and is fully consistent with it.
    (C) The submitted answer contains all the same details as the expert answer.
    (D) There is a disagreement between the submitted answer and the expert answer.
    (E) The answers differ, but these differences don't matter from the perspective of factuality.
choice_strings: ABCDE
"""

SHORT_STORY = """
Once upon a time, in a quaint village nestled between rolling hills and whispering woods, there lived a young girl named Lily. Lily was known throughout the village for her boundless curiosity and adventurous spirit.
One sunny morning, as she wandered through the forest, Lily stumbled upon a hidden path she had never noticed before. Intrigued, she followed the winding trail deeper into the woods until she reached a clearing bathed in golden sunlight.
In the center of the clearing stood a majestic oak tree, its branches reaching toward the sky like outstretched arms. Beneath the tree sat an old man with kind eyes and a gentle smile.
"Welcome, young traveler," the old man greeted Lily. "I am the Guardian of the Oak, keeper of ancient wisdom and secrets. You have been chosen to embark on a quest of great importance."
Intrigued and excited, Lily listened as the Guardian spoke of a legendary treasure hidden deep within the heart of the forest. Only a pure-hearted soul, guided by courage and compassion, could unlock its secrets and bring balance to the world.
With determination shining in her eyes, Lily accepted the challenge. With the Guardian's guidance, she ventured forth into the enchanted forest, facing trials and tribulations along the way.
Through dark forests and treacherous mountains, Lily's courage never wavered. Along the journey, she encountered magical creatures and made unlikely allies, each offering their own wisdom and assistance.
Finally, after many trials and hardships, Lily reached the heart of the forest and discovered the fabled treasure—a shimmering crystal that radiated with ancient power.
As she held the crystal aloft, a brilliant light filled the forest, banishing darkness and bringing new life to the land. The balance between light and shadow was restored, and peace reigned once more.
With the treasure in hand, Lily returned to the village as a hero, her bravery and kindness celebrated by all. Though her adventure had come to an end, her journey had only just begun, for she knew that the magic of the forest would always be a part of her.
And so, with a heart full of hope and wonder, Lily embarked on her next great adventure, ready to face whatever challenges the future might hold. For in her, the spirit of the forest lived on, a beacon of light in a world filled with darkness.
"""

SHORT_STORY_SUMMARY = """
In a quiet village, a young girl named Lily, known for her adventurous spirit, discovers a hidden path while exploring the nearby forest. Along this path, she meets Sage, an old wanderer with vast knowledge and wisdom. Intrigued by Sage's tales, Lily joins him on a quest to find the fabled City of Dreams. Together, they face numerous challenges and obstacles but persevere with determination. Finally reaching the City of Dreams, they find inner peace and fulfillment, realizing that the true magic of their journey lies in their shared experiences. Grateful for their bond and the adventures ahead, Lily and Sage sit together, ready to embrace whatever comes next.
"""