from typing import Annotated, Any
from enum import Enum
import datetime

from fastapi import APIRouter, Security, Depends, HTTPException
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app.core.db.app import engine_db, get_db
from app.schemas import PageResponseSchemas

from app.schemas.__system__.auth import UserSchemas
from app.services.__system__.auth import get_active_user

router = APIRouter(
    prefix="/data",
    tags=["FORM"],
)
pageResponse = PageResponseSchemas("templates", "pages/data/")
db: Session = Depends(get_db)
req_page = Annotated[PageResponseSchemas, Depends(pageResponse.page)]
req_depends = Annotated[PageResponseSchemas, Depends(pageResponse.pageDepends)]
req_nonAuth = Annotated[PageResponseSchemas, Depends(pageResponse.pageDependsNonUser)]
c_user_scope = Annotated[UserSchemas, Security(get_active_user, scopes=["pages"])]


class PathJS(str, Enum):
    indexJs = "index.js"
    formJs = "form.js"


###PAGES###############################################################################################################
@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def data(req: req_page):
    return pageResponse.response("index.html")


@router.get("/{cId}/{sId}/{app_version}/{pathFile}", response_class=HTMLResponse, include_in_schema=False)
def page_js(req: req_nonAuth, pathFile: PathJS):
    req.state.islogsave = False
    return pageResponse.response(pathFile)


###DATATABLES##########################################################################################################
from app.models import RepositoryTable, RepositorySizeTable
from sqlalchemy import select, func, desc
from datatables import DataTable


@router.post("/{cId}/{sId}/datatables", status_code=202, include_in_schema=False)
def get_datatables(params: dict[str, Any], req: req_depends, c_user: c_user_scope) -> dict[str, Any]:
    query = (
        select(
            RepositoryTable,
            RepositorySizeTable.size,
            RepositorySizeTable.count,
            RepositoryTable.id.label("DT_RowId"),
            func.row_number().over(order_by=desc(RepositoryTable.created_at)).label("row_number"),
        )
        .join(RepositoryTable._SIZE)
        .filter(
            RepositoryTable.deleted_at == None,
        )
    )

    datatable: DataTable = DataTable(
        request_params=params,
        table=query,
        column_names=[
            "DT_RowId",
            "id",
            "key",
            "repository",
            "desc",
            "size",
            "count",
            "created_at",
            "row_number",
        ],
        engine=engine_db,
        # callbacks=callbacks,
    )
    return datatable.output_result()
