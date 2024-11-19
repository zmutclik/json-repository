from typing import Annotated, Dict
from datetime import datetime
from fastapi import APIRouter, Request, Security, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db.app import get_db

from app.schemas.__system__.auth import UserSchemas
from app.repositories import Repository, FolderRepository, DocumentRepository, RefServerRepository
from .__helper import get_repo, get_folder
from app.services.__system__.auth import get_active_user
from app.services.document import DocumentSave, DocumentOpen
from app.schemas.document import DocumentSchemas, DocumentUpload
from app.repositories import Repository, FolderRepository, DocumentRepository

router = APIRouter(
    prefix="",
    tags=["DOCUMENT"],
)

db: Session = Depends(get_db)
c_user_scope = Annotated[UserSchemas, Security(get_active_user, scopes=[])]


@router.get("/json/{user_access}/{repo}/{key}", response_model=Dict, summary="Get Single Document JSON")
def get_single(repo: str, key: str, req: Request, db=db):
    """
    - **User Access** : diganakan untuk LOG user yang akses Dokumen ini
    - **repo** : Repository Key atau bisa juga berisi Nama Repository
    - **key** : key disini adalah key Dokumen JSON
    """
    repo_ = get_repo(Repository(db), repo)
    file = DocumentRepository(db).getKey(key)
    if file is None:
        raise HTTPException(status_code=400, detail="File Tidak ada.")
    return DocumentOpen(file.path, key)


@router.get("/folder/{user_access}/{repo}/{folder}", response_model=Dict, summary="Get All Document JSON in Folder")
def get_in_folder(repo: str, folder: str, user_access: str, req: Request, db=db):
    """
    - **User Access** : diganakan untuk LOG user yang akses Dokumen ini
    - **repo** : Repository Key atau bisa juga berisi Nama Repository
    - **folder** : Folder Key atau bisa juga berisi Nama Folder
    """
    repo_ = get_repo(Repository(db), repo)
    fold_ = get_repo(FolderRepository(db), folder)
    files = DocumentRepository(db).all(fold_.id)
    result = {}
    for item in files:
        result[item.label] = DocumentOpen(item.path, item.key)
    return result


@router.post("/json", response_model=DocumentSchemas, summary="Upload Document JSON in NEW Folder")
async def upload_document(dataIn: DocumentUpload, req: Request, c_user: c_user_scope, db=db):
    """
    Upload Dokumen JSON yang Foldernya dibuatkan Baru dengan nama Folder disamakan dengan Folder Key yang dibuat Random.

    - **repo** : Repository Key atau bisa juga berisi Nama Repository
    - **folder** : Tidak Wajib di isi, Folder Key atau bisa juga berisi Nama Folder
    - **label** : Tidak Wajib di isi, Nama Dokumen
    - **data** : berisi data yang ingin di simpan
    """
    repo_ = get_repo(Repository(db), dataIn.repo)
    fold_ = get_repo(FolderRepository(db), dataIn.folder)
    if dataIn.folder is None:
        fold_ = FolderRepository(db).create_random(repo_.key, c_user.username)

    document_key = DocumentRepository(db).create_key()
    document_label = dataIn.label
    if document_label is None:
        document_label = document_key

    document_path = DocumentSave(dataIn.data, repo_.key, fold_.key, document_key)
    document_data = DocumentSchemas(
        folder_id=fold_.id,
        folder_key=fold_.key,
        repo_key=repo_.key,
        key=document_key,
        path=document_path,
        label=document_label,
        created_user=c_user.username,
    )

    return DocumentRepository(db).create(document_data.model_dump())
