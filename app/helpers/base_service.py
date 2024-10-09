from passlib.utils.decor import print_function
from sqlalchemy.orm import Session
from pydantic import BaseModel as SchemaModel
from sqlalchemy.orm.loading import instances
from helpers.base_model import BaseModel
import shortuuid

def update_model(cls,db:Session,validated_data:SchemaModel,instance:BaseModel,is_partial:bool=False):
    ...

def save_model(cls,db:Session,validated_data:SchemaModel,model:BaseModel):
    instance =cls(**{validated_data})
    instance.uid=shortuuid.uuid()
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance

def delete_model(cls,db:Session,uid:str,force_delete=False):
    instance=db.query(cls).filter(cls.uid==uid).first()
    if force_delete:
        db.delete(instance)
    else:
        instance.is_deleted=True
        instance.is_active=False
        db.commit()

def model_detail(cls,db:Session,uid:str):
    instance= db.query(cls).filter(cls.uid==uid).first()
    return instance
