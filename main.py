from dotenv import load_dotenv
from fastapi import FastAPI
from apis.files import CoreRouters

load_dotenv()
app = FastAPI()


app.include_router(CoreRouters)


@app.get("/")
def read_root():
    return "Welcome, this is a simple chat app API"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
