from fastapi import APIRouter,Depends,JSONResponse,status, HTTPException
from src.auth.models import UserCreateModel,UserLoginModel
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.services import UserService




auth_router = APIRouter()
user_service = UserService()

@auth_router.post('/signup')
async def create_account(user : UserCreateModel,
                         session : AsyncSession = Depends(get_session)):
    
    if not await user_service.user_exists(username=user.username,session=session):
        new_user = await user_service.create_user(user_data=user,session=session)
        return JSONResponse(
            content={'message': 'User created successfully', 
                     'user': new_user},
            status_code = status.HTTP_201_CREATED
        )
    else :
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Username already exists")



@auth_router.post('/login')
async def login_user():
    pass

@auth_router.post('logout')
async def revoke_token():
    pass

@auth_router.get('refresh')
async def get_new_access_token():
    pass

@auth_router.get('/me')
async def get_current_user():
    pass


