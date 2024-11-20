from typing import Union, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class RepositorySchemas(BaseModel):
    id: Optional[int] = Field(default=None, exclude=False)
    key: Optional[str] = Field(default=None, examples=["k3y"])
    repository: str = Field(examples=["repository"])
    desc: str = Field(examples=["description of repo"])
    created_user: Optional[str] = Field(default=None, exclude=False)


class RepositoryDataPut(BaseModel):
    repository: str = Field(examples=["repository"])
    desc: str = Field(examples=["description of repo"])
