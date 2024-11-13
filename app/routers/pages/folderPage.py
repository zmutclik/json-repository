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
from app.models import FolderTable
from sqlalchemy import select, create_engine
from datatables import DataTable
from app.core import config


@router.post("/{cId}/{sId}/{repo_key}/datatables", status_code=202, include_in_schema=False)
def get_datatables(repo_key: str, params: dict[str, Any], req: req_depends, c_user: c_user_scope) -> dict[str, Any]:
    DB_ENGINE = config.DATABASE.replace("repo__json", "repo_" + repo_key.lower())
    engine_db = create_engine(DB_ENGINE)

    query = select(FolderTable, FolderTable.id.label("DT_RowId")).filter(
        FolderTable.deleted_at == None,
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
            "updated_at",
            "created_at",
        ],
        engine=engine_db,
        # callbacks=callbacks,
    )
    return datatable.output_result()
