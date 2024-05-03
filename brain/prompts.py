from langchain.prompts import ChatPromptTemplate


def default_template():
    template = """You are a helpful customer support assistant that answer the following question based on this context:

    {context}

    Question: {question}

    if you don't have the answer , respond with a single word 'NoAnswer'.
    When you are finished with the conversation and answered the question, respond with a single word 'FINISHED'
    """

    prompt = ChatPromptTemplate.from_template(template)
    return prompt