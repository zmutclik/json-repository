from typing import Union, Optional, Dict
from pydantic import BaseModel
from datetime import datetime


class RepositoryData(BaseModel):
    key: Optional[str] = None
    repository: str
    desc: str


class RepositorySchemas(RepositoryData):
    id: int


class RepositorySave(RepositoryData):
    created_user: Optional[str] = None
