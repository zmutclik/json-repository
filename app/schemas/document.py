from typing import Union, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class DocumentSchemasSave(BaseModel):
    id: Optional[int] = Field(default=None)
    folder_id: Optional[int]
    repo_key: Optional[str] = Field(examples=["r3p0k3y"])
    key: Optional[str] = Field(examples=["k3y"])
    label: str = Field(examples=["nama_file"])
    path: str = Field(default="")
    size: int = Field(default=0)
    created_user: Optional[str] = Field(default=None)


class DocumentSchemas(BaseModel):
    repo_key: Optional[str] = Field(examples=["r3p0k3y"])
    folder_key: Optional[str] = Field(examples=["F0ld3rk3y"])
    key: Optional[str] = Field(examples=["k3y"])
    label: str = Field(examples=["nama_file"])
    size: int = Field(default=0)


class DocumentUpload(BaseModel):
    repo: str = Field(examples=["r3p0"])
    folder: Optional[str] = Field(default=None, examples=["F0ld3r"])
    label: Optional[str] = Field(default=None, examples=["nama_file"])
    data: dict


class DocumentUpdate(BaseModel):
    label: str
