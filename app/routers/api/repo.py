from typing import Annotated, List
from fastapi import APIRouter, Request, Security, Depends
from sqlalchemy.orm import Session
from app.core.db.app import get_db

from app.schemas.__system__.auth import UserSchemas
from app.services.__system__.auth import get_active_user

from app.schemas.repository import RepositorySchemas

router = APIRouter(
    prefix="/repo",
    tags=["REPOSITORY"],
)

db: Session = Depends(get_db)
c_user_scope = Annotated[UserSchemas, Security(get_active_user, scopes=[])]


@router.get("/list", response_model=List[RepositorySchemas], summary="Get List All Repository Active")
def get(req: Request, c_user: c_user_scope, db=db):
    """"""
    pass


@router.get("/{repo}", response_model=RepositorySchemas, summary="Get Detail Data of Repository")
def get(repo: str, req: Request, c_user: c_user_scope, db=db):
    """
    - **repo** : Repository Key atau bisa juga berisi Nama Repository
    """
    pass


@router.put("/{repo}", summary="Update Nama atau Deskripsi Repository")
def update(repo: str, req: Request, c_user: c_user_scope, db=db):
    """
    - **repo** : Repository Key atau bisa juga berisi Nama Repository
    """
    pass
