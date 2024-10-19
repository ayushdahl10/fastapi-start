from fastapi import HTTPException
from fastapi.openapi.models import ParameterInType
from sqlalchemy.orm import Session
import shortuuid
from sqlalchemy.orm.mapper import schema
from sqlalchemy.orm.strategy_options import joinedload
from auth import models, schemas
from services import role_perm as role_crud

from helpers.auth_helper import hash_password, verify_password


def get_user(db: Session, user_id: str):
    instance = (
        db.query(models.User)
        .options(joinedload(models.User.role))
        .filter(models.User.uid == user_id)
        .first()
    )
    return instance


def create_user(db: Session, user: schemas.UserCreate):
    user.password = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        password=user.password,
        uid=shortuuid.uuid(),
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age,
        username=user.email,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_user_admin(db: Session, user: schemas.UserAdmin):
    user.password = hash_password(user.password)
    db_user = models.User(
        email=user.email,
        password=user.password,
        uid=shortuuid.uuid(),
        first_name=user.first_name,
        last_name=user.last_name,
        age=user.age,
        username=user.email,
    )
    db.add(db_user)

    # add role to user
    roles = user.roles
    if roles:
        for role in roles:
            role_instance = role_crud.get_role_by_id(db=db, role_id=role)
            db_user.role.append(role_instance)
    else:
        raise HTTPException(
            detail={"error": "roles field cannot be empty"}, status_code=400
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)


def get_user_by_email(db: Session, email: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    user = (
        db.query(models.User)
        .options(joinedload(models.User.role))
        .filter(models.User.is_active == True)
        .offset(skip)
        .limit(limit)
    )
    return user


def authenticate_user(db: Session, email: str, password: str):
    db_user = (
        db.query(models.User)
        .filter(models.User.email == email, models.User.is_active == True)
        .first()
    )
    if not db_user:
        raise HTTPException(detail="invalid email", status_code=404)
    if not verify_password(password, db_user.password):
        raise HTTPException(detail="invalid password", status_code=404)
    return db_user


def delete_user(db: Session, user_id: str):
    db_user = get_user(user_id=user_id, db=db)
    if not db_user:
        raise HTTPException(detail={"error": "user does not exists"}, status_code=400)
    db.delete(db_user)
    db.commit()


def update_user(db: Session, instance: models.User, user: schemas.UserUpdate):
    update_user = user.model_dump(exclude_unset=True)
    for key, value in update_user.items():
        setattr(instance, key, value)
    ins: schemas.User = instance
    db.commit()
    return user
