from typing import Union, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class RepositorySchemas(BaseModel):
    key: Optional[str] = Field(examples=["k3y"])
    repository: str = Field(examples=["repository"])
    desc: str = Field(examples=["description of repo"])


class RepositoryData(RepositorySchemas):
    id: int


class RepositorySave(RepositorySchemas):
    created_user: Optional[str] = None
