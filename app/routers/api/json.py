from typing import Annotated, Dict
from datetime import datetime
from fastapi import APIRouter, Request, Security, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db.app import get_db

from app.schemas.__system__.auth import UserSchemas
from app.repositories import Repository, FolderRepository, DocumentRepository, RefServerRepository
from .repo import get_repo
from app.services.__system__.auth import get_active_user
from app.services.document import DocumentSave
from app.schemas.document import DocumentSchemas, DocumentUpload

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


@router.get("/json/{user_access}/{repo_key}/{folder_key}/{key}", response_model=Dict, summary="Get All Document JSON in Folder with Spesific filter")
def get_single_spesific(user_access: str, repo_key: str, folder_key: str, key: str, req: Request, db=db):
    """
    - **User Access** : diganakan untuk LOG user yang akses Dokumen ini
    - **repo_key** : Repository Key
    - **folder_key** : Folder Key
    - **key** : Document Key
    """
    pass


@router.post("/json", response_model=DocumentSchemas, summary="Upload Document JSON in NEW Folder")
async def upload_document(dataIn: DocumentUpload, req: Request, c_user: c_user_scope, db=db):
    """
    Upload Dokumen JSON yang Foldernya dibuatkan Baru dengan nama Folder disamakan dengan Folder Key yang dibuat Random.

    - **repo_key** : Berisi Repository Key, tapi juga bisa di isi Nama Repository
    - **folder_key** : Tidak Wajib di isi, Berisi Folder Key, tapi juga bisa di isi Nama Folder
    - **label** : Tidak Wajib di isi, nama File jika kosong otomatis ber label Key File
    - **data** : berisi data yang ingin di simpan
    """
    repo = get_repo(Repository(db), dataIn.repo_key)
    folder = FolderRepository(db).getKey(dataIn.folder_key)
    if dataIn.folder_key is None:
        folder = FolderRepository(db).create_random(repo.key, c_user.username)

    document_key = DocumentRepository(db).create_key()
    document_label = dataIn.label
    if document_label is None:
        document_label = document_key

    document_path = DocumentSave(dataIn.data, repo.key, folder.key, document_key)
    document_data = DocumentSchemas(
        folder_id=folder.id,
        folder_key=folder.key,
        repo_key=repo.key,
        key=document_key,
        path=document_path,
        label=document_label,
        created_user=c_user.username,
    )

    return DocumentRepository(db).create(document_data.model_dump())
