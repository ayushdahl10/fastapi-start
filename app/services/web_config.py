from fastapi.exceptions import HTTPException
from fastapi.openapi.models import Schema
from sqlalchemy.orm.strategy_options import joinedload
from sqlalchemy.orm import Session

from web import models
from web.schemas import WebConfigCreate

import shortuuid

def create_web_config(db:Session,web_config:WebConfigCreate):
    web_config_obj= models.WebConfig(uid=shortuuid.uuid(),key=web_config.key,value=web_config.value,config=web_config.config)
    db.add(web_config_obj)
    db.commit()
    db.refresh(web_config_obj)
    return web_config_obj


def read_all_config(db:Session,skip:int,limit:int):
    return db.query(models.WebConfig).filter(models.WebConfig.is_deleted==False).offset(skip).limit(limit)
