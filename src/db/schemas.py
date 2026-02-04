from sqlmodel import SQLModel,Field,Column
from sqlalchemy.dialects import postgresql as pg
from uuid import UUID
from src.db.main import init_db
import asyncio


class TenKFilings(SQLModel,table = True):
    __tablename__ =  "ten_k_filings"
    
    uid : UUID = Field(sa_column = Column(pg.UUID(as_uuid=True),
                                          primary_key=True
                                          ,nullable=False))
    
    ticker : str = Field(sa_column = Column(pg.VARCHAR,
                                            nullable = False))
    year : str
    section : str
    content : str


    
