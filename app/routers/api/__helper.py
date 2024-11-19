from fastapi import HTTPException
from app.repositories import Repository, FolderRepository


def get_repo(repo: Repository, repo_search):
    data = repo.getKey(repo_search)
    if data is None:
        data = repo.getRepo(repo_search)
    if data is None:
        raise HTTPException(status_code=400, detail="Data Tida ada.")
    return data


def get_folder(repo: FolderRepository, folder_search):
    data = repo.getKey(folder_search)
    if data is None:
        data = repo.getFolder(folder_search)
    if data is None:
        raise HTTPException(status_code=400, detail="Data Tida ada.")
    return data
