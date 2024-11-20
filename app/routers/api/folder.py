from typing import Annotated
from fastapi import APIRouter, Request, Security, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db.app import get_db

from app.schemas.__system__.auth import UserSchemas
from app.services.__system__.auth import get_active_user

from app.schemas.folder import FolderSchemas, FolderUpdate
from app.repositories import Repository, FolderRepository
from .__helper import get_folder, get_repo

router = APIRouter(
    prefix="/folder",
    tags=["FOLDER"],
)

db: Session = Depends(get_db)
c_user_scope = Annotated[UserSchemas, Security(get_active_user, scopes=[])]


@router.get("/{repo}/{folder}", response_model=FolderSchemas, summary="Get Detail Data of Folder")
def get(repo: str, folder: str, req: Request, c_user: c_user_scope, db=db):
    """
    - **repo** : Repository Key atau bisa juga berisi Nama Repository
    - **folder** : Folder Key atau bisa juga berisi Nama Folder
    """
    repo_ = get_repo(Repository(db), repo)
    return get_folder(FolderRepository(db), folder)


@router.put("/{repo}/{folder}", response_model=FolderSchemas, summary="Update Detail Data of Folder")
def update(repo: str, folder: str, dataIn: FolderUpdate, req: Request, c_user: c_user_scope, db=db):
    """
    - **repo** : Repository Key atau bisa juga berisi Nama Repository
    - **folder** : Folder Key atau bisa juga berisi Nama Folder
    """
    repo_ = get_repo(Repository(db), repo)
    fold_ = get_folder(FolderRepository(db), folder)

    folder = FolderRepository(db).getFolder(dataIn.folder)
    if folder is not None:
        raise HTTPException(status_code=400, detail="Nama Folder Sudah ada yang Menggunakan.")

    return FolderRepository(db).update(fold_.id, {"folder": dataIn.folder})
