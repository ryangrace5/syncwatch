from fastapi import FastAPI

app = FastAPI(title="SyncWatch")

# Sample records while we build the application.
connections = [
    {"id": 1, "name": "My First Connection", "status": "healthy"},
    {"id": 2, "name": "Demo Office B", "status": "failed"},
]


@app.get("/")
def home():
    return {"message": "SyncWatch is running"}


@app.get("/connections")
def get_connections():
    return connections