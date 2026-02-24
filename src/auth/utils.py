from passlib.context import CryptContext
from src.config import Config
from src.auth.models import User
from datetime import datetime,timedelta
from uuid import uuid4
import jwt
import logging

context = CryptContext(schemes=["bcrypt"])
ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(password : str):
    return context.hash(password)

def verify_password(password : str,hash :str):
    return context.verify(password,hash)

def create_token(user_data : dict, refresh : bool = False, expiry : timedelta = None):
    JWT_SECRET = Config.JWT_SECRET
    ALGORITHM = Config.JWT_ALGORITHM

    payload = {}
    payload['user'] = user_data
    payload['expiry'] = datetime.utcnow()+ expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRY)
    payload['jti'] = str(uuid4())
    payload['refresh'] = refresh
    
    token =  jwt.encode(
        payload = payload,
        key = JWT_SECRET,
        algorithm = ALGORITHM
    )
    return token

def decode_token(token : str):
    JWT_SECRET = Config.JWT_SECRET
    ALGORITHM = Config.JWT_ALGORITHM

    try:
        payload = jwt.decode(token,JWT_SECRET,algorithms=[ALGORITHM])
        return payload
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None

def create_key():
    pass



