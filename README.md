### Chat with your data app
upload your data source and chat with your data such as asking questions or providing information.

## Features
- user upload data source (doc_name, document, vector_collection, embeddings, created_at)
- user can chat with its data
- user has vector document for every source
- user can ask question about the content of a specific document (e.g., what is this article about?)
- AI respond on him/her
- save chat history in database
- generate report based on chat history

## Installation
- Clone the PR

- Create Python ENV
  - python3 -m venv `env_name`
  - source  env_name/bin/activate
  - pip install -r requirements.txt
  - Add `.env` file with  your secret keys

- Run project
  - Run: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

## API Documentation
- [Local Docs](http://127.0.0.1:8000/docs)

## Tech Stack:
- Python 3.10+
- FastAPI
- Langchain
- OpenAI - GPT3 Or GPT4
- MongoDB
- Milvus (vector db)
- uvicorn

#### ENV Keys
- MONGO_URI="xxxxxxxx"
- SECRET_KEY="xxxxxxxx"
- ALGORITHM="xxxxxxxx"
- ACCESS_TOKEN_EXPIRE_DAYS="xxxxxxxx"
- GOOGLE_API_KEY="xxxxxxxx"
- OPENAI_API_KEY="xxxxxxxx"
- MILVUS_URI="xxxxxxxx"
- MILVUS_PORT="xxxxxxxx"
- MILVUS_USER="xxxxxxxx"
- MILVUS_PASSWORD="xxxxxxxx"
- .....
