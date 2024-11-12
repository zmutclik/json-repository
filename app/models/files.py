import os
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from app.core.db import BaseRepo as Base


class FilesTable(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    repo_key = Column(String(32), index=True)
    folder_id = Column(Integer, ForeignKey("files.id"), index=True)

    key = Column(String(32), unique=True, index=True)
    label = Column(String(32), unique=True, index=True)
    path = Column(String(256))
    size = Column(Integer)

    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_user = Column(String(50), nullable=False)
    deleted_user = Column(String(50), nullable=True)

    _SAVE = relationship("FilesTable", back_populates="_FILES", uselist=False)
    _FOLDER = relationship("FilesTable", back_populates="_FILES")


class FilesSaveTable(Base):
    __tablename__ = "files_save"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    files_id = Column(Integer, ForeignKey("files.id"), index=True)

    size = Column(Integer)
    server = Column(String(32), index=True)
    uploaded = Column(DateTime, default=None)

    _FILES = relationship("FilesTable", back_populates="_SAVE")


class FolderTable(Base):
    __tablename__ = "folder"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(32), unique=True, index=True)
    folder = Column(String(32), unique=True, index=True)

    repo_key = Column(String(32), index=True)

    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_user = Column(String(50), nullable=False)
    deleted_user = Column(String(50), nullable=True)

    _FILES = relationship("FilesTable", back_populates="_FOLDER")
    _SIZE = relationship("FolderSizeTable", back_populates="_FOLDER", uselist=False)


class FolderSizeTable(Base):
    __tablename__ = "folder_size"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    folder_id = Column(Integer, ForeignKey("folder.id"), index=True)

    size = Column(Integer)

    _FOLDER = relationship("FolderTable", back_populates="_SIZE")
