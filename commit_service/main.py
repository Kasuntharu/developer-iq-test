from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
import uvicorn
import json
from typing import Union
import requests
from config.config import settings


app = FastAPI()

headers = {
        'Accept': 'application/vnd.github+json',
        'Authorization': f'Bearer {settings.GITHUB_TOKEN}'
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    # You can add logging here if you want
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

@app.exception_handler(requests.RequestException)
async def requests_exception_handler(request: Request, exc: requests.RequestException):
    # You can log the exception details here, too
    return JSONResponse(
        status_code=500,
        content={"message": "An error occurred while handling the request", "details": str(exc)},
    )

@app.get("/status")
def status():
    return  "Commit service is working properly"


# @app.get("/{user}/{u}")
# def read_root(user: str,u: int):
#     print(u)
#     url = f"https://api.github.com/users/{user}/repos"   
#     response = requests.get(url)
#     return response.json()


@app.get("/repos/{owner}/{repos}/commits")
def list_commits(owner: str, repos: str):
    url = f"https://api.github.com/repos/{owner}/{repos}/commits"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "_main_":
    uvicorn.run("_main_:app", host="0.0.0.0", port=8001, reload=True, workers=2)