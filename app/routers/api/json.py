from typing import Annotated, Dict
from fastapi import APIRouter, Request, Security, Depends
from sqlalchemy.orm import Session
from app.core.db.app import get_db

from app.schemas.__system__.auth import UserSchemas
from app.services.__system__.auth import get_active_user

router = APIRouter(
    prefix="",
    tags=["DOCUMENT"],
)

db: Session = Depends(get_db)
c_user_scope = Annotated[UserSchemas, Security(get_active_user, scopes=[])]


@router.get("/json/{user_access}/{key}", response_model=Dict, summary="Get Single Document JSON")
def get_single(req: Request, db=db):
    """
    - **User Access** : diganakan untuk LOG user yang akses Dokumen ini
    - **key** : key disini adalah key Dokumen JSON
    """
    pass


@router.get("/folder/{user_access}/{folder}", response_model=Dict, summary="Get All Document JSON in Folder")
def get_in_folder(user_access: str, folder: str, req: Request, db=db):
    """
    - **User Access** : diganakan untuk LOG user yang akses Dokumen ini
    - **folder** : Folder bisa di isi Nama Folder atau mending Folder Key agar lebih spesifik, untuk urutan pencarian di samakan dgn Folder Key dulu lagi kalau tidak ketemu dgn Nama Folder
    """
    pass


@router.get("/folder/{user_access}/{repo_key}/{folder_key}", response_model=Dict, summary="Get Single Document JSON with Spesific filter")
def get_folder_spesific(user_access: str, repo_key: str, folder_key: str, req: Request, db=db):
    """
    - **User Access** : diganakan untuk LOG user yang akses Dokumen ini
    - **repo_key** : Repository Key
    - **folder_key** : Folder Key
    """
    pass


@router.get("/{user_access}/{repo_key}/{folder_key}/{key}", response_model=Dict, summary="Get All Document JSON in Folder with Spesific filter")
def get_single_spesific(user_access: str, repo_key: str, folder_key: str, key: str, req: Request, db=db):
    """
    - **User Access** : diganakan untuk LOG user yang akses Dokumen ini
    - **repo_key** : Repository Key
    - **folder_key** : Folder Key
    - **key** : Document Key
    """
    pass


@router.post("/json/{repo}", response_model=Dict, summary="Upload Document JSON in NEW Folder")
async def upload_document(repo: str, req: Request, c_user: c_user_scope, db=db):
    """
    Upload Dokumen JSON yang Foldernya dibuatkan Baru dengan nama Folder disamakan dengan Folder Key yang dibuat Random.

    - **repo** : Berisi Repository Key, tapi juga bisa di isi Nama Repository
    """
    pass


@router.post("/json/{repo}/{folder}", response_model=Dict, summary="Upload Document JSON in Specific Exist Folder")
async def upload_document_folder(repo: str, req: Request, c_user: c_user_scope, db=db):
    """
    Upload Dokumen JSON yang tanpa membuat Folder Baru.

    - **repo** : Berisi Repository Key, tapi juga bisa di isi Nama Repository
    - **folder** : Berisi Folder Key, tapi juga bisa di isi Nama Folder
    """
    pass
