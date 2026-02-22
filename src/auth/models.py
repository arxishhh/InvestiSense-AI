from pydantic import BaseModel,Field
from uuid import UUID
from datetime import datetime



class User(BaseModel):

    uid : UUID
    username : str = Field(...,max_length=8)
    pass_hash : str = Field(...,exclude=True)
    first_name : str
    last_name : str
    email : str 
    created_at : datetime

class UserCreateModel(BaseModel):

    username : str = Field(...,max_length=8)
    password : str = Field(...,max_length=8,exclude=True)
    first_name : str
    last_name : str
    email : str

class UserLoginModel(BaseModel):

    username : str = Field(...,max_length=8)
    password : str = Field(...,max_length=8,exclude=True)

