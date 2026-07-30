from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


# title is optional here rather than required so a missing title reaches our
# Its own check below and gets a 400 with a clear message instead of FastAPI's
# generic 422 validation error
class TaskCreate(BaseModel):
    title: Optional[str] = None


# Plain list acts as the database for this stage since no real storage exists yet
# Each task is a dict here rather than a class to keep this stage lightweight
tasks = [
    {"id": 1, "title": "I will Learn FastAPI basics", "done": False},
    {"id": 2, "title": "I will Build the tasks endpoint", "done": False},
    {"id": 3, "title": "I will Test with curl", "done": True}
]


@app.get("/")
def read_root():
    # Returning a plain dict here since FastAPI serializes it to JSON automatically
    # endpoints list is hardcoded for now since /tasks is the only route that exists
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }


@app.get("/health")
def health_check():
    # No database or dependency check here since this endpoint only needs to prove
    # the server process itself is up and able to respond
    return {"status": "ok"}


@app.get("/tasks")
def get_tasks():
    # Returning the list directly since no filtering or pagination is needed yet
    return tasks


@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    # Each task id is checked one by one since tasks are stored in a simple list
    # with no index built for lookup by id
    found_task = None
    for task in tasks:
        if task["id"] == task_id:
            found_task = task
            # Loop stops here once the match is found so the remaining tasks are not checked
            break

    # 404 is raised explicitly here since a missing task is not the same as
    # an empty result. Callers rely on the status code not just the body
    if found_task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

    return found_task


@app.post("/tasks", status_code=201)
def create_task(task: TaskCreate):
    # Title is checked here since the server is the last line of defense
    # and must never assume the client sent valid data
    if not task.title or not task.title.strip():
        raise HTTPException(status_code=400, detail="Title is required and cannot be empty")

    # max is used instead of len so ids stay unique even if a task is
    # deleted later and the list length no longer matches the highest id
    next_id = max((t["id"] for t in tasks), default=0) + 1

    new_task = {"id": next_id, "title": task.title, "done": False}
    tasks.append(new_task)

    return new_task
