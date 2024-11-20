import os
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, Time, TIMESTAMP, DateTime, func, case, Float, text
from sqlalchemy.orm import column_property, relationship, deferred, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

from app.core.db import Base


class RepositoryTable(Base):
    __tablename__ = "repository"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    key = Column(String(32), unique=True, index=True)
    repository = Column(String(32), unique=True, index=True)
    desc = Column(String(256))

    created_at = Column(TIMESTAMP, nullable=False, server_default=func.now())
    updated_at = Column(TIMESTAMP, nullable=True, onupdate=func.now())
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_user = Column(String(50), nullable=False)
    deleted_user = Column(String(50), nullable=True)

    @hybrid_property
    def count(self) -> str:
        return self._SIZE.count

    @hybrid_property
    def size(self) -> str:
        return self._SIZE.size

    _SIZE = relationship("RepositorySizeTable", back_populates="_FOLDER", uselist=False)


class RepositorySizeTable(Base):
    __tablename__ = "repository_size"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    repo_id = Column(Integer, ForeignKey("repository.id"), index=True)

    size = Column(Integer)
    count = Column(Integer)

    _FOLDER = relationship("RepositoryTable", back_populates="_SIZE")
