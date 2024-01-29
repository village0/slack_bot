import os
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import GPT4All
from langchain_core.output_parsers import StrOutputParser
from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()
# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.

local_path = (
    os.getenv('MODEL_PATH')
    # replace with your desired local file path
)

import re

# Initialize the Bolt app with the token and signing secret
app = App(token=os.getenv('SLACK_APP_TOKEN'))
# If you want to use a custom model add the backend parameter
# Check https://docs.gpt4all.io/gpt4all_python.html for supported backends
llm = GPT4All(model=local_path, backend="gptj")

template = """Text :{question} 
Answer: Summarize the Slack Conversation above in English under 100 words"""

prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)


def llm_prompt(question):
    return llm_chain.invoke({"question": question})


def summarize_text(text):
    # Clean the text by removing emojis and images
    clean_text = re.sub(r':[^:]+:', '', text)  # Removes Slack emojis
    clean_text = re.sub(r'<[^>]+>', '', clean_text)  # Removes image URLs or any Slack-specific markup
    print(clean_text)
    return llm_prompt(question=clean_text)


@app.shortcut("summarize_gpt")
def mention(ack, payload, respond, client):
    ack()
    print("Bot mentioned")
    channel_id = payload["channel"]['id']
    thread_ts = payload["message_ts"]

    # Fetch the messages from the thread
    response = client.conversations_replies(channel=channel_id, ts=thread_ts)
    messages = response["messages"]

    if len(messages) > 1:
        thread_ts = messages[1]['ts']

        # Concatenate the text from the messages with the username
    text = " ".join(
        f'{client.users_info(user=message["user"])["user"]["real_name"]}: {message["text"]}' for message in
        messages)

    respond(text='Generating Summary...', thread_ts=thread_ts, response_type='ephemeral', delete_original=True,
            replace_original=True)
    summary = summarize_text(text)
    # Send the summary in the same thread
    respond(summary['text'], thread_ts=thread_ts, response_type='ephemeral', delete_original=True,
            replace_original=True)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print(llm_chain.run({ "question": "It is a long established fact that a reader will be distracted by the
    # readable content of a page when looking at its layout. The point of using Lorem Ipsum is that it has a
    # more-or-less normal distribution of letters, as opposed to using 'Content here, content here', making it look
    # like readable English. Many desktop publishing packages and web page editors now use Lorem Ipsum as their
    # default model text, and a search for 'lorem ipsum' will uncover many web sites still in their infancy. Various
    # versions have evolved over the years, sometimes by accident, sometimes on purpose (injected humour and the
    # like)."}))

    SocketModeHandler(app, os.getenv('SLACK_OAUTH_TOKEN')).start()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
