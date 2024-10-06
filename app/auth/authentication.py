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
from services import role_perm as perm_crud


oauth2_scheme= OAuth2PasswordBearer(tokenUrl="token")
api_key_header = APIKeyHeader(name='Authorization')

def user_permission(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request=kwargs.get('request')
        user=await __get_current_user(request=request)
        await __check_permissions(request=request,user=user,name=func.__name__)
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
    request.state.user= user
    return user

async def __check_permissions(request:Request,user:models.User,name:str)->bool:
    db=next(get_db())
    if user.is_superuser:
        return True
    user_roles=user.role
    method=request.method
    has_permission:bool=False
    forbitten_message=HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="you don't have permission to access this resource",
    )
    for role in user_roles:
        permission_id= perm_crud.get_permission_by_name_and_method(db=db,name=name,method=method)
        if not permission_id:
            raise forbitten_message
        has_permission=perm_crud.check_permission(db=db,role_id=role.id,permission_id=permission_id.id)
    if has_permission:
        return True
    else:
        raise forbitten_message
