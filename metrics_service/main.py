from typing import Union , Optional
from fastapi import Query
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException  # Importing HTTPException

import uvicorn
from fastapi import FastAPI
import requests
from pydantic import BaseModel
import json 

app = FastAPI()


GITHUB_USERNAME = "Kasuntharu"
ACCESS_TOKEN = "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"

BASE_URL = "https://api.github.com"




@app.get("/")
def read_root():
    return {"Hello": "World"}

#List Down users for a Repository 
@app.get("/repository_users/{owner}/{repo}")
def get_repository_users(owner: str, repo: str):
    url = f"{BASE_URL}/repos/{owner}/{repo}/contributors"

    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch repository users")

        contributors = response.json()
        users = [contributor["login"] for contributor in contributors]

        return {
            "repository": f"{owner}/{repo}",
            "users": users
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch repository users: {str(e)}")





#Getting Matrices
@app.get("/repository_metrics/{owner}/{repo}/{username}")
def get_repository_metrics(owner: str, repo: str, username: str):
    url = f"{BASE_URL}/repos/{owner}/{repo}"

    headers = {
        "Authorization": f"token {ACCESS_TOKEN}",
        "Accept": "application/vnd.github.v3+json",
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail="Failed to fetch repository details")

        repository = response.json()

        # Get commits for the repository
        commits_url = f"{BASE_URL}/repos/{owner}/{repo}/commits"
        commits_response = requests.get(commits_url, headers=headers)
        commits_data = commits_response.json()
        commits = len([commit for commit in commits_data if commit['author']['login'] == username])

        # Get pull requests for the repository
        pulls_url = f"{BASE_URL}/repos/{owner}/{repo}/pulls"
        pulls_response = requests.get(pulls_url, headers=headers)
        pull_requests_data = pulls_response.json()
        pull_requests = len([pr for pr in pull_requests_data if pr['user']['login'] == username])

        # Get issues for the repository
        issues_url = f"{BASE_URL}/repos/{owner}/{repo}/issues"
        issues_response = requests.get(issues_url, headers=headers, params={"state": "closed"})
        issues_resolved_data = issues_response.json()
        issues_resolved = len([
            issue for issue in issues_resolved_data if issue['user']['login'] == username or issue['closed_by']['login'] == username
        ])

        # Get merge requests for the repository (assuming they are equivalent to pull requests)
        merge_requests = len([pr for pr in pull_requests_data if pr['user']['login'] == username])

        return {
            "repository": f"{owner}/{repo}",
            "username": username,
            "commits": commits,
            "pull_requests": pull_requests,
            "issues_resolved": issues_resolved,
            "merge_requests": merge_requests
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch metrics: {str(e)}")



