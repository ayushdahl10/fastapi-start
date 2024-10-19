from fastapi import Depends
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from helpers.base_res import error_response
from auth import schemas
from services import auth_service as crud
from auth.auth_security import create_access_token
from manager.database import get_db


router = APIRouter()


ACCESS_TOKEN_EXPIRE_MINUTES = 30


@router.post("/register/", response_model=schemas.User, tags=["Login and Register"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        return error_response("email already registered", status_code=400)
    return crud.create_user(db=db, user=user)


@router.post("/token", tags=["Login and Register"])
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    users = crud.authenticate_user(
        db=db, email=form_data.username, password=form_data.password
    )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": users.email}, expires_delta=access_token_expires
    )
    return JSONResponse(
        content={
            "access_token": access_token,
            "user_id": users.uid,
            "token_type": "bearer",
        },
        status_code=200,
    )
