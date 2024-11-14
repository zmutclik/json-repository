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
    prefix="/repository",
    tags=["FORM"],
)

pageResponse = PageResponseSchemas("templates", "pages/repository/")
db: Session = Depends(get_db)
req_page = Annotated[PageResponseSchemas, Depends(pageResponse.page)]
req_depends = Annotated[PageResponseSchemas, Depends(pageResponse.pageDepends)]
req_nonAuth = Annotated[PageResponseSchemas, Depends(pageResponse.pageDependsNonUser)]
c_user_scope = Annotated[UserSchemas, Security(get_active_user, scopes=["admin", "pages"])]


class PathJS(str, Enum):
    indexJs = "index.js"
    formJs = "form.js"


###PAGES###############################################################################################################
from app.repositories.repository import Repository


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def page_system_repository(req: req_page):
    return pageResponse.response("index.html")


@router.get("/{cId}/{sId}/add", response_class=HTMLResponse, include_in_schema=False)
def page_system_repository_add(req: req_depends):
    return pageResponse.response("form.html")


@router.get("/{cId}/{sId}/{id:int}", response_class=HTMLResponse, include_in_schema=False)
def page_repository_form(id: int, req: req_depends, db=db):
    pageResponse.addData("data", Repository(db).get(id))
    return pageResponse.response("form.html")


@router.get("/{cId}/{sId}/{app_version}/{pathFile}", response_class=HTMLResponse, include_in_schema=False)
def page_js(req: req_nonAuth, pathFile: PathJS):
    req.state.islogsave = False
    return pageResponse.response(pathFile)


###DATATABLES##########################################################################################################
from app.models import RepositoryTable
from sqlalchemy import select
from datatables import DataTable


@router.post("/{cId}/{sId}/datatables", status_code=202, include_in_schema=False)
def get_datatables(params: dict[str, Any], req: req_depends, c_user: c_user_scope) -> dict[str, Any]:
    query = (
        select(RepositoryTable, RepositoryTable.id.label("DT_RowId"))
        .filter(
            RepositoryTable.deleted_at == None,
        )
        .order_by(RepositoryTable.repository)
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
            "created_at",
        ],
        engine=engine_db,
        # callbacks=callbacks,
    )
    return datatable.output_result()


###CRUD################################################################################################################
from app.schemas.repository import RepositorySchemas


@router.post("/{cId}/{sId}", response_model=RepositorySchemas, status_code=201, include_in_schema=False)
async def create(dataIn: RepositorySchemas, req: req_depends, c_user: c_user_scope, db=db):
    repo = Repository(db)
    data = RepositorySchemas.model_validate(dataIn.model_dump())
    data.created_user = c_user.username
    data.key = repo.create_key()
    cdata = repo.create(data.model_dump())

    return cdata


@router.post("/{cId}/{sId}/{id:int}", response_model=RepositorySchemas, status_code=202, include_in_schema=False)
async def update(dataIn: RepositorySchemas, id: int, req: req_depends, c_user: c_user_scope, db=db):
    repo = Repository(db)
    data = repo.get(id)
    if data is None:
        raise HTTPException(status_code=400, detail="Data Tida ada.")

    return repo.update(id, dataIn.model_dump())


@router.delete("/{cId}/{sId}/{id:int}", status_code=202, include_in_schema=False)
async def delete(id: int, req: req_depends, c_user: c_user_scope, db=db):
    repo = Repository(db)
    data = repo.get(id)
    if data is None:
        raise HTTPException(status_code=400, detail="Data Tida ada.")

    return repo.delete(c_user.username, id)
