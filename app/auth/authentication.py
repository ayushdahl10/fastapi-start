from fastapi import Depends,HTTPException
from typing_extensions import Annotated
from sqlalchemy.orm import Session
from auth import models,schemas
from jwt.exceptions import InvalidTokenError
from fastapi import status,Request
from fastapi.security import OAuth2PasswordBearer
from functools import wraps
from fastapi.security import APIKeyHeader

from auth.auth_security import TokenData,jwt_decode
from manager.database import get_db
from services import auth_service as crud






oauth2_scheme= OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name='Authorization')

def user_permission(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request=kwargs.get('request')
        await __get_current_user(request=request)
        result = func(*args, **kwargs)
        return result
    return wrapper


async def __get_current_user(request:Request):
    token=await oauth2_scheme(request=request,)
    db=next(get_db())
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="authentication credentials were not provided",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_decode(token=token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    user = crud.get_user_by_email(db=db,email=token_data.username)
    if user is None:
        raise credentials_exception
    request.state.user=user
    return user
