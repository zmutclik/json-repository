import re, os, json
from typing import Union
from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories import RefServerRepository
from app.models import FilesSaveTable, FolderSizeTable, RepositorySizeTable
from app.core.db.app import engine_db, get_db


def urlify(s):
    # Remove all non-word characters (everything except numbers and letters)
    s = re.sub(r"[^\w\s]", "", s)
    # Replace all runs of whitespace with a single dash
    s = re.sub(r"\s+", " ", s)
    return s


def dircheck(server_path: str, path: str, mkdir: bool = True):
    if not os.path.isdir(server_path + "/" + path):
        if mkdir:
            os.mkdir(server_path + "/" + path)
        else:
            return False
    return path


def DocumentSave(dataJSON: dict, repo_key: str, folder_key: str, key: str, creation_time: Union[datetime, None] = None):
    if creation_time is None:
        creation_time = datetime.now()

    with engine_db.begin() as connection:
        with Session(bind=connection) as db:
            refserver = RefServerRepository(db).local()
            server_path = refserver.path
            path = dircheck(server_path, "/{}".format(repo_key))
            path = dircheck(server_path, path + "/{}".format(creation_time.strftime("%Y")))
            path = dircheck(server_path, path + "/{}".format(creation_time.strftime("%m")))
            path = dircheck(server_path, path + "/{}".format(creation_time.strftime("%W")))
            path = dircheck(server_path, path + "/{}".format(creation_time.strftime("%j")))
            path = dircheck(server_path, path + "/{}".format(folder_key))

            filePath = server_path + "/" + path + "/{}".format(key)

            with open(filePath, "w") as outfile:
                json.dump(dataJSON, outfile)

            fileSize = os.path.getsize(filePath)
            return refserver.id, fileSize, path


def DocumentOpen(file_path: str, key: str):
    with engine_db.begin() as connection:
        with Session(bind=connection) as db:
            refserver = RefServerRepository(db).local()
            server_path = refserver.path
            filePath = server_path + "" + file_path + "/{}".format(key)

            if not os.path.isdir(server_path + "" + file_path):
                raise HTTPException(status_code=400, detail="Folder Tidak Tersedia.")
            if not os.path.isfile(filePath):
                raise HTTPException(status_code=400, detail="File Tidak Tersedia.")

            with open(filePath, "r") as file:
                return json.load(file)


def DocumentCalculateSize(folder_id: int, repo_id: int):
    with engine_db.begin() as connection:
        with Session(bind=connection) as db:
            folderSize = (
                db.query(func.sum(FilesSaveTable.size).label("size"), func.count(FilesSaveTable.id).label("count"))
                .filter(FilesSaveTable.folder_id == folder_id)
                .first()
            )
            db.query(FolderSizeTable).filter(FolderSizeTable.folder_id == folder_id).update({"size": folderSize.size, "count": folderSize.count})
            db.commit()
            repoSize = (
                db.query(func.sum(FolderSizeTable.size).label("size"), func.sum(FolderSizeTable.count).label("count"))
                .filter(FolderSizeTable.repo_id == repo_id)
                .first()
            )
            db.query(RepositorySizeTable).filter(RepositorySizeTable.repo_id == repo_id).update({"size": repoSize.size, "count": repoSize.count})
            db.commit()
