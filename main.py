from fastapi import FastAPI

app = FastAPI()


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
