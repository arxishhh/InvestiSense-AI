from fastapi.security import HTTPBearer
from fastapi import HTTPException,status
from fastapi import Request, Depends
from src.auth.utils import decode_token
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.services import UserService
from src.db.main import get_session

userservice =UserService()


class TokenBearer(HTTPBearer):

    def __init__(self,auto_error : bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self,request : Request):

        creds = await super().__call__(request)
        token = creds.credentials

        token_data = decode_token(token)

        if not self.validate_token(token):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid token or expired token")
        
        self.verify_token(token_data=token_data)
        return token_data

    def validate_token(self,token : str):
        token_data = decode_token(token)

        return token_data is not None
    
    def verify_token(self,token_data: dict):
        raise NotImplementedError("Subclasses must implement this method to verify the token data")


class AccessTokenBearer(TokenBearer):

    def verify_token(self,token_data : dict):
        if token_data and token_data.get('refresh'):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid token type")
        
class RefreshTokenBearer(TokenBearer):

    def verify_token(self, token_data):
        if token_data and not token_data.get('refresh'):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token type")


async def get_current_user(token_data : str = Depends(AccessTokenBearer()), session : AsyncSession = Depends(get_session)):

    username = token_data.get('user',{}).get('username')
    user = await userservice.get_user_by_username(username=username,session=session)
    return user

    


                       


