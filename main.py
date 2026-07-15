from fastapi import FastAPI

app = FastAPI(title="To-do List")


@app.get("/")
async def root():
    return {"message": "Hello World"}
