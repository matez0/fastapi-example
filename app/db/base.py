import databases
from pydantic import BaseSettings
import sqlalchemy
from sqlalchemy.orm import declarative_base


class Settings(BaseSettings):
    ms_database_url = 'sqlite:///./test.db'


settings = Settings()

database = databases.Database(settings.ms_database_url)

metadata = sqlalchemy.MetaData()

engine = sqlalchemy.create_engine(settings.ms_database_url, connect_args={'check_same_thread': False})

Base = declarative_base(metadata=metadata)
