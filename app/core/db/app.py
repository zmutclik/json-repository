from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core import config

from app.models import RepositoryTable, RefServerTable

# https://www.tutorialspoint.com/sqlalchemy/sqlalchemy_orm_textual_sql.htm
engine_db = create_engine(config.DATABASE)
conn_db = engine_db.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False)
SessionLocal.configure(
    binds={
        #############################################
        RefServerTable: engine_db,
        #############################################
        RepositoryTable: engine_db,
    }
)
if not engine_db.dialect.has_table(table_name="repository", connection=conn_db):
    from . import Base

    Base.metadata.create_all(bind=engine_db)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
