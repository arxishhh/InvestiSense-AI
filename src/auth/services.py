from src.auth.models import UserCreateModel
from src.db.schemas import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.auth.utils import generate_password_hash,verify_password

class UserService():

    async def create_user(self,user_data : UserCreateModel,session : AsyncSession):

        user_data_dict =user_data.model_dump(exclude={'password'})
        new_user = User(**user_data_dict)

        new_user.pass_hash = generate_password_hash(user_data.password)

        session.add(new_user)
        await session.commit()

        return new_user
    
    async def get_user_by_username(self,username : str,session : AsyncSession):

        query = select(User).where(User.username == username)
        result = await session.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self,email : str,session : AsyncSession):

        query = select(User).where(User.email == email)
        result = await session.execute(query)

        return result.scalar_one_or_none()
    
    async def user_exists(self,email : str,username : str,session : AsyncSession):

        user = await self.get_user_by_username(username,session)
        user_email = await self.get_user_by_email(email,session)

        return user is not None and user_email is not None
    
    async def authenticate_user(self,email : str,password : str,session : AsyncSession):

        user = await self.get_user_by_email(email,session)

        if user and verify_password(password,user.pass_hash):
            return user
        
        return None
