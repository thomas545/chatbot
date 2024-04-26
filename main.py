from dotenv import load_dotenv
from fastapi import FastAPI
# from auth.apis import users_routers
# from chats.apis import chats_routers

load_dotenv()
app = FastAPI()


# app.include_router(users_routers)
# app.include_router(chats_routers)


@app.get("/")
def read_root():
    return "Welcome, this is a simple chat app API"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
