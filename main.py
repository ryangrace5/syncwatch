import httpx
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

@app.get("/check")
def check_api(simulate_failure: bool = False):
    url = "https://api.github.com"

    # A deliberately missing address lets us test a failure.
    if simulate_failure:
        url += "/syncwatch-demo-missing-endpoint"

    try:
        response = httpx.get(
            url,
            timeout=5.0,
            headers={"User-Agent": "SyncWatch"},
        )

        successful = 200 <= response.status_code < 300

        return {
            "url": url,
            "status": "healthy" if successful else "failed",
            "http_status": response.status_code,
        }

    except httpx.TimeoutException:
        return {
            "url": url,
            "status": "failed",
            "http_status": None,
            "error": "The connection timed out.",
        }

    except httpx.RequestError as error:
        return {
            "url": url,
            "status": "failed",
            "http_status": None,
            "error": str(error),
        }