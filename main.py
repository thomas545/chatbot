from lang_chain import store_get_vectors, ChatOpenAI, run

collection_name = "xxxxxx"
# urls = [
#     "https://www.mosaicml.com/blog/mpt-7b",
#     "https://stability.ai/blog/stability-ai-launches-the-first-of-its-stablelm-suite-of-language-models",
#     "https://lmsys.org/blog/2023-03-30-vicuna/",
# ]
# docs = splitter(urls)
# vector_store = store_get_vectors(docs, collection_name)

vector_store = store_get_vectors([], collection_name)
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)

question = "explain How big is stableLM?"
result = run(question, llm, vector_store, [])
print(result["answer"])
