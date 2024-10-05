from helpers.base_model import BaseModel,Base
from sqlalchemy import JSON, String, Column

class WebConfig(BaseModel):
    __tablename__='web_config'

    key= Column(String,default="",unique=True,index=True)
    value= Column(String,default="",nullable=False)
    config= Column(JSON, default={})
