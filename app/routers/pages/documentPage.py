from typing import Annotated, Any, Dict
from enum import Enum
import datetime

from fastapi import APIRouter, Security, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.schemas import PageResponseSchemas

from app.schemas.__system__.auth import UserSchemas
from app.services.__system__.auth import get_active_user
from app.services.document import DocumentOpen
from app.repositories import Repository, FolderRepository, DocumentRepository
from app.core.db.app import engine_db, get_db

router = APIRouter(
    prefix="/document",
    tags=["FORM"],
)
pageResponse = PageResponseSchemas("templates", "pages/document/")
db: Session = Depends(get_db)
req_page = Annotated[PageResponseSchemas, Depends(pageResponse.page)]
req_depends = Annotated[PageResponseSchemas, Depends(pageResponse.pageDepends)]
req_nonAuth = Annotated[PageResponseSchemas, Depends(pageResponse.pageDependsNonUser)]
c_user_scope = Annotated[UserSchemas, Security(get_active_user, scopes=["pages"])]


class PathJS(str, Enum):
    indexJs = "index.js"
    formJs = "form.js"


###PAGES###############################################################################################################
@router.get("/{repo_key}/{folder_key}", response_class=HTMLResponse, include_in_schema=False)
def data_folder(repo_key: str, folder_key: str, req: req_page):
    pageResponse.addData("repo_key", repo_key)
    pageResponse.addData("folder_key", folder_key)
    return pageResponse.response("index.html")


@router.get("/{cId}/{sId}/{app_version}/{repo_key}/{folder_key}/{pathFile}", response_class=HTMLResponse, include_in_schema=False)
def page_js(repo_key: str, folder_key: str, req: req_nonAuth, pathFile: PathJS):
    pageResponse.addData("repo_key", repo_key)
    pageResponse.addData("folder_key", folder_key)
    req.state.islogsave = False
    return pageResponse.response(pathFile)


@router.get("/{cId}/{sId}/{repo_key}/{folder_key}/{key}", response_model=Dict)
def get_data(repo_key: str, folder_key: str, key: str, req: req_page, db=db):
    repo = Repository(db).getKey(repo_key)
    if repo is None:
        raise HTTPException(status_code=400, detail="Repo Tidak ada.")
    fold = FolderRepository(db).getKey(folder_key)
    if fold is None:
        raise HTTPException(status_code=400, detail="Folder Tidak ada.")
    file = DocumentRepository(db).getKey(key)
    if file is None:
        raise HTTPException(status_code=400, detail="Data Tidak ada.")

    return DocumentOpen(file.path, key)


###DATATABLES##########################################################################################################
from app.models import FilesTable
from sqlalchemy import select, func, desc
from datatables import DataTable
from app.core import config
from app.repositories import FolderRepository


@router.post("/{cId}/{sId}/{repo_key}/{folder_key}/datatables", status_code=202, include_in_schema=False)
def get_datatables(repo_key: str, folder_key: str, params: dict[str, Any], req: req_depends, c_user: c_user_scope, db=db) -> dict[str, Any]:
    folder = FolderRepository(db).getKey(folder_key)
    query = select(
        FilesTable,
        FilesTable.key.label("DT_RowId"),
        func.row_number().over(order_by=desc(FilesTable.created_at)).label("row_number"),
    ).filter(FilesTable.deleted_at == None, FilesTable.repo_key == repo_key, FilesTable.folder_id == folder.id)
    datatable: DataTable = DataTable(
        request_params=params,
        table=query,
        column_names=[
            "DT_RowId",
            "id",
            "key",
            "repo_key",
            "label",
            "size",
            "updated_at",
            "created_at",
            "created_user",
            "row_number",
        ],
        engine=engine_db,
        # callbacks=callbacks,
    )
    return datatable.output_result()
