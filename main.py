from contextlib import asynccontextmanager
from os import getenv
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


class Task(SQLModel, table=True):
    id: int | None = Field(index=True, default=None, primary_key=True)
    title: str | None = Field(index=True)
    done: bool = Field(default=False)


class TaskCreate(SQLModel):
    title: str | None = Field(default=None, min_length=1)
    done: bool = Field(default=False)


class taskUpdate(SQLModel):
    title: str | None = Field(default=None)
    done: bool | None = Field(default=None)


load_dotenv()

sqlite_url = getenv("DATABASE_URL")

if not sqlite_url:
    raise ValueError("DATABASE_URL is not set in environment variables or .env file")

engine = create_engine(sqlite_url)


def create_db_and_table():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        task_count = len(session.exec(select(Task)).all())

        if task_count == 0:
            tasks = [
                Task(id=1, title="buy bread", done=True),
                Task(id=2, title="Clean room", done=False),
                Task(id=3, title="buy milk", done=True),
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
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="API health")
def health():
    return {"status": "ok"}


@app.get("/tasks", summary="List all the tasks", response_model=list[Task])
def list_tasks(session: SessionDeps):
    tasks = session.exec(select(Task)).all()
    return tasks


@app.get("/tasks/{id}", summary="List a specific task by id", response_model=Task)
def list_task(id: int, session: SessionDeps):
    task = session.exec(select(Task).where(Task.id == id)).first()
    if task:
        return task
    raise HTTPException(status_code=404, detail={"error": f"Task {id} not found"})


@app.post("/tasks", summary="Create new tasks", response_model=Task)
def create_task(task: TaskCreate, session: SessionDeps):

    if task.title is None or task.title == "":
        raise HTTPException(status_code=400, detail={"Bad request": "title is missing"})
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


@app.put("/tasks/{id}", summary="update existing task", response_model=Task)
def update_task(id: int, update_task: taskUpdate, session: SessionDeps):
    if update_task.title is None and update_task.done is None:
        raise HTTPException(status_code=400, detail={"error": "Empty Body"})

    db_task = session.get(Task, id)
    if not db_task:
        raise HTTPException(status_code=404, detail={"error": "unknown id"})
    task_data = update_task.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.delete("/tasks/{id}", summary="Delete task")
def delete_task(id: int, session: SessionDeps):

    task = session.get(Task, id)
    if not task:
        raise HTTPException(status_code=404, detail={"error": "Unknown id"})

    session.delete(task)
    session.commit()
    return {}
