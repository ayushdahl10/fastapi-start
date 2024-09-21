from fastapi import Depends,HTTPException
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic_core.core_schema import TaggedUnionSchema
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import Integer, String
from typing_extensions import List

from helpers.base_res import success_response,error_response
from auth import schemas
from manager import SessionLocal
from services import role_perm as crud
from fastapi.security import OAuth2PasswordBearer
from auth.apis.users  import get_current_active_user
from fastapi import Response
from manager.database import get_db

router=APIRouter(prefix="/api/v1")


@router.post("/roles",response_model=schemas.Role,tags=['Role'])
def create_role(role:schemas.CreateRole,db:Session= Depends(get_db), current_user: schemas.User = Depends(get_current_active_user)):
    check_role_exists=crud.get_role_by_name(db,role.name)
    if check_role_exists:
        raise HTTPException(detail={"error":f"role already exists with name {role.name}"},status_code=400)
    role=crud.create_role(db=db,role=role)
    return role


@router.delete("/roles/{role_id}",tags=['Role'])
def delete_role(role_id:str,db:Session=Depends(get_db),current_user:schemas.User=Depends(get_current_active_user)):
    deleted= crud.delete_role(force=True,role_id=role_id,db=db)
    return success_response("Role deleted successfully")

@router.get("/roles",response_model=List[schemas.Role],tags=['Role'])
def get_all_roles(db:Session=Depends(get_db),current_user:schemas.User=Depends(get_current_active_user)):
    roles=crud.get_roles(db)
    return roles


@router.get("/roles/{role_id}",tags=['Role'],response_model=schemas.RoleDetail)
def get_role_by_id(role_id:str,db:Session=Depends(get_db),current_user:schemas.User=Depends(get_current_active_user)):
    role=crud.get_role_by_id(role_id=role_id,db=db)
    if not role:
        raise HTTPException(detail={"error":f"role not found with id= {role_id}"})
    return role

@router.patch("/roles/{role_id}",tags=['Role'],response_model=schemas.RoleDetail)
def update_role_by_id(role_id:str,role:schemas.CreateRolePermissions,db:Session=Depends(get_db),current_user:schemas.User=Depends(get_current_active_user)):
    ...
