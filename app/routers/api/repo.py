from typing import Annotated, List
from fastapi import APIRouter, Request, Security, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db.app import get_db

from app.schemas.__system__.auth import UserSchemas
from app.services.__system__.auth import get_active_user

from app.schemas.repository import RepositorySchemas, RepositoryDataPut
from app.repositories.repository import Repository

router = APIRouter(
    prefix="/repo",
    tags=["REPOSITORY"],
)

db: Session = Depends(get_db)
c_user_scope = Annotated[UserSchemas, Security(get_active_user, scopes=[])]


@router.get("/list", response_model=List[RepositorySchemas], summary="Get List All Repository Active")
def get(req: Request, c_user: c_user_scope, db=db):
    """"""
    return Repository(db).all()


def get_data(repo: Repository, repo_search):
    data = repo.getKey(repo_search)
    if data is None:
        data = repo.getRepo(repo_search)
    return data


@router.get("/{repo}", response_model=RepositorySchemas, summary="Get Detail Data of Repository")
def get(repo: str, req: Request, c_user: c_user_scope, db=db):
    """
    - **repo** : Repository Key atau bisa juga berisi Nama Repository
    """
    r3po = Repository(db)
    data = get_data(r3po, repo)
    if data is None:
        raise HTTPException(status_code=400, detail="Data Tida ada.")

    return data


@router.put("/{repo}", response_model=RepositorySchemas, summary="Update Nama atau Deskripsi Repository")
def update(dataIn: RepositoryDataPut, repo: str, req: Request, c_user: c_user_scope, db=db):
    """
    - **repo** : Repository Key atau bisa juga berisi Nama Repository
    """
    r3po = Repository(db)
    data = get_data(r3po, repo)
    if data is None:
        raise HTTPException(status_code=400, detail="Data Tida ada.")

    return r3po.update(data.id, dataIn.model_dump())
