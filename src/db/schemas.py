from sqlmodel import SQLModel,Field,Column
from sqlalchemy.dialects import postgresql as pg
from uuid import UUID
from src.db.main import init_db
import datetime
import asyncio


class User(SQLModel,table=True):
    __tablename__ = 'users'

    id : UUID = Field(sa_column=Column(pg.UUID(as_uuid=True),
                                       primary_key=True,
                                       default=UUID))
    
    username : str = Field(sa_column=Column('username',pg.VARCHAR(8),unique = True,nullable=False))
    email : str 
    first_name : str
    last_name : str
    pass_hash : str = Field(exclude = True)
    created_at : datetime.datetime = Field(sa_column=Column('created-at',pg.TIMESTAMP,
                                                            default=datetime.datetime.utcnow))

    



    
