from fastapi import Depends,HTTPException
from fastapi import APIRouter,Request
from sqlalchemy.orm import Session
from fastapi.security.api_key import APIKeyHeader

from helpers.base_res import success_response,error_response
from auth import schemas
from services import auth_service as crud
from manager.database import get_db
from auth.authentication import user_permission

router=APIRouter()
api_key_header = APIKeyHeader(name='Authorization')

router.dependencies=[Depends(api_key_header)]

ACCESS_TOKEN_EXPIRE_MINUTES=30

@router.get("/users/me/", response_model=schemas.User,tags=['Auth'])
@user_permission
def read_users_me(request:Request,api_key=Depends(api_key_header)):
    user_me:schemas.User=request.state.user
    return user_me

@router.post("/users",tags=['Auth'])
@user_permission
def create_user_admin(user:schemas.UserAdmin,db:Session=Depends(get_db),api_key=Depends(api_key_header)):
    check_email=crud.get_user_by_email(db=db,email=user.email)
    if check_email:
        raise HTTPException(detail={"error":f"user already exists for email= {user.email}"},status_code=400)
    instance= crud.create_user_admin(db=db,user=user)
    return success_response(content="user created successfully",status_code=200)

@router.get("/users/", response_model=list[schemas.User],tags=['Auth'])
@user_permission
def get_users(request:Request,skip: int = 0, limit: int = 100, db: Session = Depends(get_db),api_key=Depends(api_key_header)):
    users = crud.get_users(db,skip=skip,limit=limit)
    return users

@user_permission
@router.get("/users/{user_id}",response_model=schemas.User,tags=['Auth'])
def get_user_by_id(user_id:str,db:Session=Depends(get_db),api_key=Depends(api_key_header)):
    users=crud.get_user(db,user_id)
    if users is None:
        return error_response(f"object not found with uid = {user_id}",status_code=404)
    return users


@user_permission
@router.delete("/users/{user_id}",tags=['Auth'])
def delete_user(user_id:str,db:Session=Depends(get_db),api_key=Depends(api_key_header)):
    crud.delete_user(db=db,user_id=user_id)
    return success_response("User deleted successfully")
