from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="To-do List")
tasks = [
    {"id": 1, "title": "buy bread", "done": True},
    {"id": 2, "title": "Clean room", "done": False},
    {"id": 3, "title": "buy milk", "done": True},
]


@app.get("/")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/tasks")
async def list_tasks():
    return tasks


@app.get("/tasks/{id}")
async def list_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})
