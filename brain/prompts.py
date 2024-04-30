from langchain.prompts import ChatPromptTemplate


def default_template():
    template = """You are a helpful assistant that answer the following question based on this context:

    {context}

    Question: {question}
    """

    prompt = ChatPromptTemplate.from_template(template)
    return prompt