from fastapi import Depends,HTTPException,Request
from fastapi import APIRouter
from sqlalchemy.orm import Session
from starlette import status
from typing_extensions import List

from helpers.base_res import success_response
from auth import schemas
from services import role_perm as crud
from manager.database import get_db
from auth.authentication import user_permission
from fastapi.security.api_key import APIKeyHeader

router=APIRouter()

api_key_header = APIKeyHeader(name='Authorization')

router.dependencies=[Depends(api_key_header)]


@router.post("/roles",response_model=schemas.Role,tags=['Role'])
@user_permission
def create_role(request:Request,role:schemas.CreateRole,db:Session= Depends(get_db)):
    check_role_exists=crud.get_role_by_name(db,role.name)
    if check_role_exists:
        raise HTTPException(detail={"error":f"role already exists with name {role.name}"},status_code=400)
    role=crud.create_role(db=db,role=role)
    return role

@router.delete("/roles/{role_id}",tags=['Role'])
@user_permission
def delete_role(request:Request,role_id:str,db:Session=Depends(get_db)):
    deleted= crud.delete_role(force=True,role_id=role_id,db=db)
    return success_response("Role deleted successfully")

@router.get("/roles",response_model=List[schemas.Role],tags=['Role'])
@user_permission
def get_all_roles(request:Request,db:Session=Depends(get_db)):
    roles=crud.get_roles(db)
    return roles

@router.get("/roles/{role_id}",tags=['Role'],response_model=schemas.RoleDetail)
@user_permission
def get_role_by_id(request:Request,role_id:str,db:Session=Depends(get_db)):
    role=crud.get_role_by_id(role_id=role_id,db=db)
    if not role:
        raise HTTPException(detail={"error":f"role not found with id= {role_id}"},status_code=status.HTTP_404_NOT_FOUND)
    return role

@router.patch("/roles/{role_id}",tags=['Role'],response_model=schemas.RoleDetail)
@user_permission
def update_role_by_id(request:Request,role_id:str,role:schemas.CreateRolePermissions,db:Session=Depends(get_db)):
    ...
