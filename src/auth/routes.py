from fastapi import APIRouter,Depends,JSONResponse,status, HTTPException
from src.auth.models import UserCreateModel,UserLoginModel
from src.db.main import get_session
from src.auth.utils import verify_password,create_token
from sqlmodel.ext.asyncio.session import AsyncSession
from src.auth.services import UserService
from src.auth.dependency import AccessTokenBearer,RefreshTokenBearer
from datetime import timedelta,datetime
from src.exceptions import *
from src.db.redis import add_jti_to_blocklist


REFRESH_TOKEN_EXPIRY = 2

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
        raise UserAlreadyExists()

@auth_router.post('/login')
async def login_user(login_data : UserLoginModel, session : AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password

    user = await user_service.authenticate_user(email=email,password=password,session=session)

    if user:
        if verify_password(password,user.pass_hash):
            access_token = create_token(user_data={
                'email':email,
                'user_uid':str(user.uid)
            },refresh=False)
            refresh_token = create_token(user_data={
                'email':email,
                'user_uid':str(user.uid)
            },refresh=True,
            expiry=timedelta(days=REFRESH_TOKEN_EXPIRY))

            return JSONResponse(
                content={
                    'message':'Login Successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user':{
                        "email":email,
                        "uid":str(user.uid)
                        }},status_code=status.HTTP_200_OK)
    
    raise InvalidCredentials()

    

@auth_router.post('/logout')
async def revoke_token(token_details : dict = Depends(AccessTokenBearer)):
    jti = token_details.get('jti')
    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            "message":"Logout successful"
        },
        status_code=status.HTTP_200_OK
    )

@auth_router.get('/refresh')
async def get_new_access_token(token_data : dict = Depends(RefreshTokenBearer)) -> JSONResponse:
    expiry_timestamp = token_data.get('expiry')
    if datetime.utcfromtimestamp(expiry_timestamp) > datetime.utcnow():
        new_access_token = create_token(user_data=token_data.get('user'),refresh=False)

        return JSONResponse(
            content={
                "access_token":new_access_token
            })
    raise InvalidToken()

