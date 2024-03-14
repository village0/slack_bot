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

TEXT = """
I love books but you know, it's kinda hard to keep up with the new ones esp in the non-fiction genre.
"""

REPHRASED_TEXT = """
I have a passion for books, but I find it challenging to stay updated with new releases, especially in the non-fiction genre.
"""

INFORMAL_EMAIL = """
Subject: Time Off Request 🌴
Hey Joe,
I hope you're doing awesome! 😊
Just wanted to drop you a quick note to ask for a bit of time off. Feeling a bit burnt out and could really use a breather. Thinking of taking 5 off starting from 1st April to 5th April.
I'll make sure to wrap up any loose ends before I go and keep everyone in the loop so things run smoothly while I'm out.
Let me know if you need anything else from me!
Thanks a bunch!
Cheers,
Jane
"""

FORMAL_EMAIL = """
Subject: Request for Leave of Absence
Dear Mr. Joe,
I trust this email finds you well.
I am writing to formally request some time off from work. Due to recent circumstances, I find myself in need of a short break to recharge and address personal matters. Specifically, I am considering taking 5 off, commencing from 1st April to 5th April.
Rest assured, I will ensure that all pending tasks are completed and properly handed over before my departure. Additionally, I will maintain communication with my colleagues to ensure continuity of workflow during my absence.
Please do not hesitate to reach out if you require any further information or clarification.
Thank you for your understanding and consideration.
Warm regards,
Jane
"""

EXPLANATION = """
Multithreading in Python refers to the capability of a Python program to execute multiple threads concurrently within a single process. A thread is a sequence of instructions within a program that can run independently, allowing different parts of the program to execute simultaneously.
Python provides a built-in module called `threading` to facilitate multithreading. This module allows developers to create and manage threads, enabling tasks to be executed concurrently. Threads share the same memory space within a process, making it easy for them to communicate and interact with each other.
Multithreading is particularly useful in scenarios where a program needs to handle multiple tasks simultaneously, such as performing I/O operations (reading from and writing to files, network communication) or executing tasks in parallel to improve performance.
However, it's important to note that Python's Global Interpreter Lock (GIL) can limit the effectiveness of multithreading, especially in CPU-bound scenarios where threads compete for CPU resources. Despite this limitation, multithreading can still be beneficial for I/O-bound tasks, allowing programs to make better use of available resources and improve overall efficiency.
"""

IDEATION = """
Increasing productivity at work can be achieved through various strategies and initiatives. Here are some ideas to consider:
1. **Set Clear Goals and Priorities**: Establish clear, achievable goals for individuals and teams. Prioritize tasks based on importance and deadlines to ensure that efforts are focused on the most critical activities.
2. **Implement Time Management Techniques**: Encourage the use of time management techniques such as the Pomodoro Technique or time blocking to improve focus and productivity. Provide training or resources to help employees effectively manage their time.
3. **Provide Adequate Resources and Tools**: Ensure that employees have access to the necessary resources, tools, and technology to perform their tasks efficiently. Invest in software, equipment, and training to streamline workflows and eliminate unnecessary manual processes.
4. **Promote Work-Life Balance**: Encourage a healthy work-life balance by offering flexible work arrangements, such as remote work options or flexible hours. Promote regular breaks and discourage working overtime excessively to prevent burnout and improve overall well-being.
5. **Encourage Collaboration and Communication**: Foster a culture of collaboration and open communication within teams. Encourage regular meetings, brainstorming sessions, and knowledge sharing to facilitate collaboration and innovation.
6. **Provide Opportunities for Skill Development**: Offer opportunities for employees to enhance their skills and knowledge through training programs, workshops, or certifications. Invest in professional development to empower employees and improve job satisfaction.
7. **Streamline Processes and Eliminate Bottlenecks**: Identify and eliminate inefficiencies in workflows and processes. Streamline procedures, automate repetitive tasks, and remove bottlenecks to improve workflow efficiency and productivity.
8. **Set Realistic Deadlines and Expectations**: Ensure that deadlines and expectations are realistic and achievable. Avoid overloading employees with excessive workloads or unrealistic timelines, as this can lead to stress and decreased productivity.
9. **Encourage Breaks and Physical Activity**: Encourage employees to take regular breaks and engage in physical activity throughout the day. Physical activity can improve mood, concentration, and overall well-being, leading to increased productivity.
10. **Recognize and Reward Performance**: Acknowledge and reward employees for their hard work and contributions. Recognize achievements, milestones, and outstanding performance to motivate employees and reinforce positive behaviors.
11. **Monitor Progress and Provide Feedback**: Regularly monitor progress towards goals and provide constructive feedback to employees. Offer guidance, support, and mentorship to help employees improve their performance and achieve their objectives.
12. **Promote a Positive Work Environment**: Cultivate a positive work environment characterized by trust, respect, and collaboration. Encourage teamwork, celebrate successes, and address any issues or conflicts promptly to maintain a positive atmosphere conducive to productivity.
By implementing these strategies and fostering a culture of productivity, organizations can effectively increase efficiency, engagement, and overall performance in the workplace.
"""