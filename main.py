from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlmodel import Field, Session, SQLModel, create_engine, select


class TaskBase(SQLModel, table=True):
    id: int | None = Field(index=True, default=None, primary_key=True)
    title: str | None = Field(index=True)
    done: bool = Field(default=False)


sqlite_file_name = "tasks.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_table():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        task_count = len(session.exec(select(TaskBase)).all())

        if task_count == 0:
            tasks = [
                TaskBase(id=1, title="buy bread", done=True),
                TaskBase(id=2, title="Clean room", done=False),
                TaskBase(id=3, title="buy milk", done=True),
            ]
            session.add_all(tasks)
            session.commit()


def get_session():
    with Session(engine) as session:
        yield session


@asynccontextmanager
async def on_startup(app: FastAPI):
    create_db_and_table()
    yield


SessionDeps = Annotated[Session, Depends(get_session)]
app = FastAPI(title="To-do List", lifespan=on_startup)


@app.get("/", summary="API description")
async def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="API health")
async def health():
    return {"status": "ok"}


@app.get("/tasks", summary="List all the tasks")
async def list_tasks():
    return tasks


@app.get("/tasks/{id}", summary="List a specific task by id")
async def list_task(id: int):
    for task in tasks:
        if task["id"] == id:
            return task
    return JSONResponse(status_code=404, content={"error": f"Task {id} not found"})


@app.post("/tasks", summary="Create new tasks")
async def create_task(title: str):

    if title is None or title == "":
        return JSONResponse(
            status_code=400, content={"Bad request": "title is missing"}
        )

    next_id = max((task["id"] for task in tasks), default=0) + 1

    new_task = {"id": next_id, "title": title, "done": False}

    tasks.append(new_task)

    return JSONResponse(status_code=201, content={"status": "done. New task added"})


@app.put("/tasks/{id}", summary="update existing task")
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


@app.delete("/tasks/{id}", summary="Delete task")
async def delete_task(id: int):
    for task in tasks:
        if task["id"] == id:
            tasks.remove(task)
            return JSONResponse(
                status_code=204, content={"status": "task deleted successfully"}
            )

    return JSONResponse(status_code=404, content={"error": "Unknown id"})
