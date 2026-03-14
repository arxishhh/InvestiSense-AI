from sqlmodel import SQLModel,Field,Column
from sqlalchemy.dialects import postgresql as pg
from uuid import UUID,uuid4
import datetime


class User(SQLModel,table=True):
    __tablename__ = 'users'

    uid : UUID = Field(sa_column=Column(pg.UUID(as_uuid=True),
                                       primary_key=True,
                                       default=uuid4))
    
    username : str = Field(sa_column=Column('username',pg.VARCHAR(8),unique = True,nullable=False))
    email : str 
    first_name : str
    last_name : str
    pass_hash : str = Field(exclude = True)
    created_at : datetime.datetime = Field(sa_column=Column('created-at',pg.TIMESTAMP,
                                                            default=datetime.datetime.utcnow))

    



    
