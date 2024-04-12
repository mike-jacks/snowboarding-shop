from sqlmodel import SQLModel, create_engine, Session

from models import Snowboard

database_name = "database.db"
sqlite_url = f"sqlite:///data/{database_name}"

engine = create_engine(sqlite_url, echo=True)
SQLModel.metadata.create_all(engine)