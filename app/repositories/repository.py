from datetime import datetime
from sqlalchemy.orm import Session
from app.models import RepositoryTable as MainTable, RepositorySizeTable as SizeTable
from key_generator.key_generator import generate as key_generator
from app.core.db.repo import create_folder
from app.core.config import config


class Repository:
    def __init__(self, db_session: Session) -> None:
        self.session = db_session

    def get(self, id: int):
        return self.session.query(MainTable).filter(MainTable.id == id, MainTable.deleted_at == None).first()

    def all(self):
        return self.session.query(MainTable).filter(MainTable.deleted_at == None).order_by(MainTable.repository).all()

    def getKey(self, key: str):
        return self.session.query(MainTable).filter(MainTable.key == key, MainTable.deleted_at == None).first()

    def getRepo(self, repo: str):
        return self.session.query(MainTable).filter(MainTable.repository == repo, MainTable.deleted_at == None).first()

    def create_key(self):
        passkey = key_generator(1, "", config.MIN_KEY, config.MAX_KEY, type_of_value="hex", capital="mix", extras=[]).get_key()
        check_db = self.getKey(passkey)
        if check_db is not None:
            return self.create_key()
        else:
            return passkey

    def create(self, dataIn):
        data = MainTable(**dataIn)
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)

        create_folder(data.key)

        size = SizeTable(**{"repo_id": data.id, "size": 0, "count": 0})
        self.session.add(size)
        self.session.commit()

        return data

    def update(self, id: int, dataIn: dict):
        dataIn_update = dataIn if type(dataIn) is dict else dataIn.__dict__
        dataIn_update["updated_at"] = datetime.now()
        (self.session.query(MainTable).filter(MainTable.id == id).update(dataIn_update))
        self.session.commit()
        return self.get(id)

    def delete(self, username: str, id_: int) -> None:
        self.update(id_, {"deleted_at": datetime.now(), "deleted_user": username})
