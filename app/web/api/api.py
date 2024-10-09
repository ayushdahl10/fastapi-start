from fastapi import Depends,HTTPException
from fastapi import APIRouter,Request
import shortuuid
from sqlalchemy.orm import Session
from fastapi.security.api_key import APIKeyHeader
from typing_extensions import List
from auth.authentication import user_permission
from web import schemas,models

from helpers.base_res import success_response,error_response
from manager.database import get_db
from auth.authentication import user_permission
from services import web_config as crud
from helpers.base_service import model_detail

router=APIRouter()
api_key_header = APIKeyHeader(name='Authorization')

router.dependencies=[Depends(api_key_header)]

@router.post("/web_config",response_model=schemas.WebConfigBase,tags=["Config"])
@user_permission
def create_web_config(request:Request,web_config:schemas.WebConfigCreate,db:Session=Depends(get_db)):
    web_config_obj=crud.create_web_config(db=db,web_config=web_config)
    return web_config_obj

@router.get("/web_config",tags=["Config"],response_model=List[schemas.WebConfigDetail])
@user_permission
def get_all_web_config(request:Request,db:Session=Depends(get_db)):
    return crud.read_all_config(db=db,skip=0,limit=10)

@router.patch("/web_config/{uid}",tags=["Config"],response_model=schemas.WebConfigDetail)
@user_permission
def update_web_config(request:Request,uid:str,web_config:schemas.WebConfigCreate,db:Session=Depends(get_db)):
    instance= crud.get_config_by_id(db=db,uid=uid)
    updated_instance= crud.update_web_config(db=db,web_config=web_config,instance=instance)
    return updated_instance

@router.get("/web_config/{uid}",tags=["Config"],response_model=schemas.WebConfigDetail)
@user_permission
def get_config_detail(request:Request,uid:str,db:Session=Depends(get_db)):
    instance= model_detail(db=db,uid=uid,cls=models.WebConfig)
    return instance
