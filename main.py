from fastapi import FastAPI, HTTPException

app = FastAPI()

# Plain list acts as the database for this stage since no real storage exists yet
# Each task is a dict here rather than a class to keep this stage lightweight
tasks = [
    {"id": 1, "title": "Learn FastAPI basics", "done": False},
    {"id": 2, "title": "Build the tasks endpoint", "done": False},
    {"id": 3, "title": "Test with curl", "done": True}
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
