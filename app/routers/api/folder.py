from typing import Annotated
from fastapi import APIRouter, Request, Security, Depends
from sqlalchemy.orm import Session
from app.core.db.app import get_db

from app.schemas.__system__.auth import UserSchemas
from app.services.__system__.auth import get_active_user

from app.schemas.folder import FolderSchemas

router = APIRouter(
    prefix="/folder",
    tags=["FOLDER"],
)

db: Session = Depends(get_db)
c_user_scope = Annotated[UserSchemas, Security(get_active_user, scopes=[])]


@router.get("/{folder}", response_model=FolderSchemas, summary="Get Detail Data of Folder")
def get(folder: str, req: Request, c_user: c_user_scope, db=db):
    """
    - **folder** : Folder Key atau bisa juga berisi Nama Folder
    """
    pass


@router.put("/{folder}", response_model=FolderSchemas, summary="Update Detail Data of Folder")
def update(folder: str, req: Request, c_user: c_user_scope, db=db):
    """
    - **folder** : Folder Key atau bisa juga berisi Nama Folder
    """
    pass
