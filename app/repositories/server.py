from datetime import datetime
from sqlalchemy.orm import Session
from app.models import RefServerTable as MainTable
from app.core.config import config


class RefServerRepository:
    def __init__(self, db_session: Session) -> None:
        self.session = db_session

    def get(self, id: int):
        return self.session.query(MainTable).filter(MainTable.id == id, MainTable.deleted_at == None).first()

    def default(self):
        return self.session.query(MainTable).filter(MainTable.default == True, MainTable.deleted_at == None).first()

    def local(self):
        return self.session.query(MainTable).filter(MainTable.id == 1, MainTable.deleted_at == None).first()

    def all(self):
        return self.session.query(MainTable).filter(MainTable.deleted_at == None).order_by(MainTable.metode, MainTable.name).all()

    def create(self, dataIn):
        data = MainTable(**dataIn)
        self.session.add(data)
        self.session.commit()
        self.session.refresh(data)
        return data

    def update(self, id: int, dataIn: dict):
        dataIn_update = dataIn if type(dataIn) is dict else dataIn.__dict__
        dataIn_update["updated_at"] = datetime.now()
        (self.session.query(MainTable).filter(MainTable.id == id).update(dataIn_update))
        self.session.commit()
        return self.get(id)

    def delete(self, username: str, id_: int) -> None:
        self.update(id_, {"deleted_at": datetime.now(), "deleted_user": username})
