from typing import Union, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime


class DocumentSchemas(BaseModel):
    id: Optional[int] = Field(default=None, exclude=False)
    folder_id: Optional[int] = Field(exclude=False)
    repo_key: Optional[str] = Field(examples=["r3p0_k3y"])
    folder_key: Optional[str] = Field(examples=["F0ld3r_k3y"])
    key: Optional[str] = Field(examples=["k3y"])
    label: str = Field(examples=["nama_file"])
    path: str = Field(default="", exclude=False)
    size: int = Field(default=0)
    created_user: Optional[str] = Field(default=None, exclude=False)


class DocumentUpload(BaseModel):
    repo_key: str = Field(examples=["r3p0_k3y"])
    folder_key: Optional[str] = Field(default=None, examples=["F0ld3r_k3y"])
    label: Optional[str] = Field(default=None, examples=["nama_file"])
    data: dict
