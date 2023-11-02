import uvicorn
from typing import Union

from fastapi import FastAPI
import requests
app = FastAPI()


# @app.get("/{user}/{u}")
# def read_root(user: str,u: int):
#     print(u)
#     url = f"https://api.github.com/users/{user}/repos"   
#     response = requests.get(url)
#     return response.json()

@app.get("/commits")
def read_root():
    # print(u)
    url = f"https://api.github.com/repos/kasuntharu/developer-iq/commits"   
    response = requests.get(url)
    return response.json()

# @app.get("/items/{item_id}")
# def read_item(item_id: int, q: Union[str, None] = None):
#     return {"item_id": item_id, "q": q}

if __name__ == "_main_":
    uvicorn.run("_main_:app", host="0.0.0.0", port=8000, reload=True, workers=2)