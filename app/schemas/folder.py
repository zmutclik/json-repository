from typing import Union, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class FolderSchemas(BaseModel):
    key: Optional[str] = Field(examples=["k3y"])
    repo_key: Optional[str] = Field(examples=["rEp0k3y"])
    folder: str = Field(examples=["folder"])
    count: int
    size: int


class FolderData(FolderSchemas):
    id: int


class FolderUpdate(BaseModel):
    folder: str
