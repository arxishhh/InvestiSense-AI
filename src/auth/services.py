from src.auth.models import UserCreateModel,UserLoginModel,User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select
from src.auth.utils import generate_password_hash,verify_password

class UserService():

    async def create_user(self,user_data : UserCreateModel,session : AsyncSession):

        user_data_dict =user_data.model.dump(exclude={'password'})

        new_user = User(**user_data_dict)
        new_user.pass_hash = generate_password_hash(user_data.password)

        session.add(new_user)
        await session.commit()

        return new_user
    
    async def get_user_by_username(self,username : str,session : AsyncSession):

        query = select(User).where(User.username == username)

        result = await session.execut(query)
        return result.first()
    
    async def user_exists(self,username : str,session : AsyncSession):

        user = await self.get_user_by_username(username,session)

        return user is not None