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


class CrudMixin:
    """Provides a database independent API for create, retrieve, update, delete operation.

    Attributes needed to be created in the derived class:

    obj: the model class of the database table which is a subclass of `Base`.
    from_orm: factory to create a subclass instance.
    """

    obj: Base
    from_orm: type(classmethod)

    @classmethod
    async def create(cls, **values):
        query = cls.obj.__table__.insert().values(**values)
        return cls(**values, id=await database.execute(query))

    @classmethod
    async def get(cls, **conditions):
        query = cls.obj.__table__.select()

        if conditions:
            query = query.where(*[getattr(cls.obj, key) == value for key, value in conditions.items()])

        return [cls.from_orm(item) for item in await database.fetch_all(query)]

    @classmethod
    async def update(cls, id, **values):
        query = cls.obj.__table__.update().where(cls.obj.id == id).values(**values)
        return cls(**values, id=id) if await database.execute(query) else None

    @classmethod
    async def delete(cls, id):
        query = cls.obj.__table__.delete().where(cls.obj.id == id)
        return await database.execute(query)
