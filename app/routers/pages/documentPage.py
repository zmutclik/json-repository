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

router = APIRouter(
    prefix="/document",
    tags=["FORM"],
)
pageResponse = PageResponseSchemas("templates", "pages/document/")
# db: Session = Depends(get_db)
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
def page_js(repo_key: str, folder_key: str, key: str, req: req_page):
    return DocumentOpen(repo_key, folder_key, key)


###DATATABLES##########################################################################################################
from app.models import FilesTable
from sqlalchemy import select, func, desc
from datatables import DataTable
from app.core import config
from app.core.db.app import engine_db, get_db
from app.repositories import FolderRepository


@router.post("/{cId}/{sId}/{repo_key}/{folder_key}/datatables", status_code=202, include_in_schema=False)
def get_datatables(
    repo_key: str, folder_key: str, params: dict[str, Any], req: req_depends, c_user: c_user_scope, db: Session = Depends(get_db)
) -> dict[str, Any]:
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
            "updated_at",
            "created_at",
            "row_number",
        ],
        engine=engine_db,
        # callbacks=callbacks,
    )
    return datatable.output_result()
