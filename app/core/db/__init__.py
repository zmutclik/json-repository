from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
BaseRepo = declarative_base()
BaseLogs = declarative_base()
BaseAuth = declarative_base()
BaseSysT = declarative_base()
BaseSeSS = declarative_base()

__all__ = [
    "Base",
    "BaseRepo",
    "BaseLogs",
    "BaseAuth",
    "BaseSysT",
    "BaseSeSS",
]
