from fastapi import Depends,HTTPException
from fastapi import APIRouter,Request
import shortuuid
from sqlalchemy.orm import Session
from fastapi.security.api_key import APIKeyHeader
from auth.authentication import user_permission
from web import schemas,models

from helpers.base_res import success_response,error_response
from manager.database import get_db
from auth.authentication import user_permission
from services import web_config as crud

router=APIRouter()
api_key_header = APIKeyHeader(name='Authorization')

router.dependencies=[Depends(api_key_header)]

@router.post("/web_config",response_model=schemas.WebConfigCreate,tags=["Web Config"])
@user_permission
def create_web_config(request:Request,web_config:schemas.WebConfigCreate,db:Session=Depends(get_db)):
    web_config=crud.create_web_config(db=db,web_config=web_config)
    return web_config

@router.get("/web_config",tags=["Web Config"])
@user_permission
def get_all_web_config(request:Request,db:Session=Depends(get_db)):
    ...
