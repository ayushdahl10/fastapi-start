from fastapi import HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel as SchemaModel
from helpers.base_model import BaseModel
import shortuuid


def update_model(
    cls,
    db: Session,
    update_payload: SchemaModel,
    instance: BaseModel,
    is_partial: bool = False,
):
    updated_payload = update_payload.model_dump(exclude_unset=is_partial)
    for key, value in updated_payload.items():
        setattr(instance, key, value)
    db.commit()
    return instance


def save_model(cls, db: Session, validated_data: SchemaModel):
    validated_data = dict(validated_data)
    instance = cls.from_dict(validated_data)
    if not instance.uid:
        instance.uid = shortuuid.uuid()
    try:
        db.add(instance)
        db.commit()
    except Exception as e:
        raise e
    db.refresh(instance)
    return instance


def delete_model(cls, db: Session, uid: str, force_delete=False):
    instance = db.query(cls).filter(cls.uid == uid, cls.is_deleted == False).first()
    if not instance:
        raise HTTPException(status_code=404, detail=f"no object found with uid= {uid}")
    if force_delete:
        db.delete(instance)
    else:
        instance.is_deleted = True
        instance.is_active = False
    db.commit()


def model_detail(cls, db: Session, uid: str):
    instance = db.query(cls).filter(cls.uid == uid, cls.is_deleted == False).first()
    return instance


def model_list(cls, db: Session):
    query = db.query(cls).filter(cls.is_deleted == False)
    return query
