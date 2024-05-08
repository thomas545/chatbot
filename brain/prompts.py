from langchain.prompts import ChatPromptTemplate


def default_template():
    template = """You are a helpful customer support assistant that choose the proper tool to answer the question.

    Here is a chat history to help you understand the pervious chat between customer and you
    {chat_history}

    Question: {query}

    {agent_scratchpad}
    """

    prompt = ChatPromptTemplate.from_template(template)
    return prompt


# """
    # When you are finished with the conversation and answered the question, respond with a single word 'FINISHED'

#     if the user complain with the issue generate a random ticket number from 10 digits and reply with your ticket number is: xxx. in response
#     if you don't have the answer , respond with a single word 'I don't know the answer' and generate a random ticket number from 10 digits and reply with your ticket number is: xxx. in response.
# """
