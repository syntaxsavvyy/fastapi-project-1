from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def new():
    return "Hello World!"
