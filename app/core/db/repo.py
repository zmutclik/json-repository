from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from app.core import config
from app.core.db import BaseRepo
from app.models.files import FolderTable, FolderSizeTable, FilesTable, FilesSaveTable


def create_folder(repo_key: str):
    DB_ENGINE = config.DATABASE.replace("repo__json", "repo_" + repo_key.lower())
    print("DB_ENGINE = ", DB_ENGINE)
    print("create_database = ", DB_ENGINE)
    create_database(DB_ENGINE)
    engine_db = create_engine(DB_ENGINE)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False)
    SessionLocal.configure(
        binds={
            FolderTable: engine_db,
            FolderSizeTable: engine_db,
            FilesTable: engine_db,
            FilesSaveTable: engine_db,
        }
    )
    BaseRepo.metadata.create_all(bind=engine_db)


# # Dependency
# def get_db(repo_key: str):
#     DB_ENGINE = config.DATABASE.replace("repo__json", "repo_" + repo_key.lower())
#     print("DB_ENGINE = ", DB_ENGINE)

#     if not database_exists(DB_ENGINE):
#         print("create_database = ", DB_ENGINE)
#         create_database(DB_ENGINE)

#     engine_db = create_engine(DB_ENGINE)
#     conn_db = engine_db.connect()

#     SessionLocal = sessionmaker(autocommit=False, autoflush=False)
#     SessionLocal.configure(
#         binds={
#             FolderTable: engine_db,
#             FolderSizeTable: engine_db,
#             FilesTable: engine_db,
#             FilesSaveTable: engine_db,
#         }
#     )
#     if not engine_db.dialect.has_table(table_name="files", connection=conn_db):
#         from . import BaseRepo as Base

#         Base.metadata.create_all(bind=engine_db)

#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
