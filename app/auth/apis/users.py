from fastapi import Depends,HTTPException
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Integer, String
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone
from fastapi import status
from jwt.exceptions import InvalidTokenError
from fastapi import Response


from helpers.base_res import success_response,error_response
from auth import schemas
from manager import SessionLocal
from services import auth_service as crud
from fastapi.security import OAuth2PasswordBearer
from auth.auth_security import create_access_token,Token,TokenData,jwt_decode
from manager.database import get_db

router=APIRouter()

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES=30

@router.post("/register/", response_model=schemas.User,tags=['Login and Register'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user =crud.get_user_by_email(db, email=user.email)
    if db_user:
        return error_response("email already registered",status_code=400)
    return crud.create_user(db=db, user=user)

@router.post("/token",tags=['Login and Register'])
def login (form_data:Annotated[OAuth2PasswordRequestForm,Depends()],db:Session=Depends(get_db)):
    users= crud.authenticate_user(db=db,email=form_data.username,password=form_data.password)
    access_token_expires= timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token= create_access_token(data={'sub':users.email},expires_delta=access_token_expires)
    return JSONResponse(content={'access_token':access_token,'user_id':users.uid,'token_type':'bearer'},status_code=200)

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],db:Session=Depends(get_db)):
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
    return user

def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    if current_user.is_active==False:
        raise HTTPException(status_code=400, detail=f"Inactive user {current_user.email}")
    return current_user

@router.get("/users/me/", response_model=schemas.User,tags=['Auth'])
def read_users_me(
    current_user: Annotated[schemas.User, Depends(get_current_active_user)],
):
    return current_user

@router.post("/users",tags=['Auth'])
def create_user_admin(user:schemas.UserAdmin,db:Session=Depends(get_db),current_user:schemas.User=Depends(get_current_active_user)):
    check_email=crud.get_user_by_email(db=db,email=user.email)
    if check_email:
        raise HTTPException(detail={"error":f"user already exists for email= {user.email}"},status_code=400)
    instance= crud.create_user_admin(db=db,user=user)
    return success_response(content="user created successfully",status_code=200)


@router.get("/users/", response_model=list[schemas.User],tags=['Auth'])
def get_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    users = crud.get_users(db,skip=skip,limit=limit)
    return users


@router.get("/users/{user_id}",response_model=schemas.User,tags=['Auth'])
def get_user_by_id(user_id:str,db:Session=Depends(get_db),current_user: schemas.User = Depends(get_current_active_user)):
    users=crud.get_user(db,user_id)
    if users is None:
        return error_response(f"object not found with uid = {user_id}",status_code=404)
    return users


@router.delete("/users/{user_id}",tags=['Auth'])
def delete_user(user_id:str,db:Session=Depends(get_db),current_user:schemas.User=Depends(get_current_active_user)):
    crud.delete_user(db=db,user_id=user_id)
    return success_response("User deleted successfully")
