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


@app.post("/tasks")
async def create_task(title: str):

    if title is None or title == "":
        return JSONResponse(
            status_code=400, content={"Bad request": "title is missing"}
        )

    next_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {"id": next_id, "title": title, "done": False}

    tasks.append(new_task)

    return JSONResponse(status_code=201, content={"status": "done. New task added"})


@app.put("/tasks/{id}")
async def update_task(id: int, new_title: str | None = None, done: bool | None = None):
    if new_title is None and done is None:
        return JSONResponse(status_code=400, content={"error": "Empty Body"})

    for task in tasks:
        if task["id"] == id:
            if new_title is not None and new_title != "":
                task["title"] = new_title

            if done is not None:
                task["done"] = done

            return task

    return JSONResponse(status_code=404, content={"error": "unknown id"})


@app.delete("/tasks/{id}")
async def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return JSONResponse(
                status_code=204, content={"status": "task deleted successfully"}
            )

    return JSONResponse(status_code=404, content={"error": "Unknown id"})
