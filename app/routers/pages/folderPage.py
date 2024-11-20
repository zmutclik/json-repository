from typing import Annotated, Any
from enum import Enum
import datetime

from fastapi import APIRouter, Security, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.schemas import PageResponseSchemas

from app.schemas.__system__.auth import UserSchemas
from app.services.__system__.auth import get_active_user

router = APIRouter(
    prefix="/folder",
    tags=["FORM"],
)
pageResponse = PageResponseSchemas("templates", "pages/folder/")
# db: Session = Depends(get_db)
req_page = Annotated[PageResponseSchemas, Depends(pageResponse.page)]
req_depends = Annotated[PageResponseSchemas, Depends(pageResponse.pageDepends)]
req_nonAuth = Annotated[PageResponseSchemas, Depends(pageResponse.pageDependsNonUser)]
c_user_scope = Annotated[UserSchemas, Security(get_active_user, scopes=["pages"])]


class PathJS(str, Enum):
    indexJs = "index.js"
    formJs = "form.js"


###PAGES###############################################################################################################
@router.get("/{repo_key}", response_class=HTMLResponse, include_in_schema=False)
def data_folder(repo_key: str, req: req_page):
    pageResponse.addData("repo_key", repo_key)
    return pageResponse.response("index.html")


@router.get("/{cId}/{sId}/{app_version}/{repo_key}/{pathFile}", response_class=HTMLResponse, include_in_schema=False)
def page_js(repo_key: str, req: req_nonAuth, pathFile: PathJS):
    pageResponse.addData("repo_key", repo_key)
    req.state.islogsave = False
    return pageResponse.response(pathFile)


###DATATABLES##########################################################################################################
from app.models import FolderTable, FolderSizeTable
from sqlalchemy import select, func, desc
from datatables import DataTable
from app.core import config
from app.core.db.app import engine_db


@router.post("/{cId}/{sId}/{repo_key}/datatables", status_code=202, include_in_schema=False)
def get_datatables(repo_key: str, params: dict[str, Any], req: req_depends, c_user: c_user_scope) -> dict[str, Any]:
    query = (
        select(
            FolderTable,
            FolderSizeTable.size,
            FolderSizeTable.count,
            FolderTable.id.label("DT_RowId"),
            func.row_number().over(order_by=desc(FolderTable.created_at)).label("row_number"),
        )
        .join(FolderTable._SIZE)
        .filter(FolderTable.deleted_at == None, FolderTable.repo_key == repo_key)
    )
    datatable: DataTable = DataTable(
        request_params=params,
        table=query,
        column_names=[
            "DT_RowId",
            "id",
            "key",
            "repo_key",
            "folder",
            "size",
            "count",
            "updated_at",
            "created_at",
            "row_number",
        ],
        engine=engine_db,
        # callbacks=callbacks,
    )
    return datatable.output_result()
