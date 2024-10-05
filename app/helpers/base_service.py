from sqlalchemy.orm import Session
from pydantic import BaseModel as SchemaModel
from helpers.base_model import BaseModel

def update_model(db:Session,validated_data:SchemaModel,instance:BaseModel,is_partial:bool=False):
    ...

def save_model(db:Session,validated_data:SchemaModel):
    ...

def delete_model(db:Session,id:int):
    ...
