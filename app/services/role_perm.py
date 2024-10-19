from fastapi.exceptions import HTTPException
from fastapi.openapi.models import Schema
from sqlalchemy.orm.strategy_options import joinedload
from sqlalchemy.orm import Session

from auth import schemas
from auth import models
import shortuuid


# permission services


def delete_all_permissions(db: Session):
    db.query(models.Permissions).delete()


def create_permissions(db: Session, permission: schemas.Permission):
    db_permission = models.Permissions(
        url_path=permission.url_path,
        uid=shortuuid.uuid(),
        name=permission.name,
        method=permission.method,
    )
    db.add(db_permission)
    db.commit()
    return db_permission


def get_permission_by_url(db: Session, url_path: str):
    db_perm = (
        db.query(models.Permissions)
        .filter(models.Permissions.url_path == url_path)
        .first()
    )
    return db_perm


def get_permission_by_url_and_method(db: Session, url_path: str, method: str):
    db_perm = (
        db.query(models.Permissions)
        .filter(
            models.Permissions.url_path == url_path, models.Permissions.method == method
        )
        .first()
    )
    return db_perm


def get_permission_by_name(db: Session, name: str):
    db_perm = (
        db.query(models.Permissions).filter(models.Permissions.name == name).first()
    )
    return db_perm


def get_permission_by_name_and_method(db: Session, name: str, method: str):
    method = method.upper()
    db_perm = (
        db.query(models.Permissions)
        .filter(models.Permissions.name == name, models.Permissions.method == method)
        .first()
    )
    return db_perm


def get_permission_by_id(db: Session, uid: str):
    db_perm = db.query(models.Permissions).filter(models.Permissions.uid == uid).first()
    return db_perm


def update_permissions(db: Session, permission: schemas.Permission): ...


# role services


def create_role(db: Session, role: schemas.CreateRole):
    db_role = models.Roles(
        is_active=role.is_active, name=role.name, uid=shortuuid.uuid()
    )
    db.add(db_role)
    db.commit()
    return db_role


def update_roles_with_permissions(db: Session, permissions: list, role_name: str):
    db_role = get_role_by_name(db=db, role_name=role_name.lower())
    print(db_role)
    # adding permissions to role
    permissions = permissions
    if permissions:
        for permission in permissions:
            permission_obj = get_permission_by_id(db=db, uid=permission)
            db_role.permission.append(permission_obj)
    db.commit()
    return db_role


def get_roles(db: Session):
    roles = db.query(models.Roles).filter()
    return roles


def get_role_by_id(db: Session, role_id: str):
    role_instance = (
        db.query(models.Roles)
        .options(joinedload(models.Roles.permission))
        .filter(models.Roles.uid == role_id)
        .first()
    )
    if not role_instance:
        raise HTTPException(
            detail={"error": f"not role found for id= {role_id}"}, status_code=404
        )
    return role_instance


def get_role_by_name(db: Session, role_name: str):
    role = db.query(models.Roles).filter(models.Roles.name == role_name).first()
    return role


def delete_role(role_id: str, db: Session, force: bool = False):
    if force:
        role = db.query(models.Roles).filter(models.Roles.uid == role_id).first()
        if not role:
            raise HTTPException(
                detail={"error": f"no role found with id= {role_id}"}, status_code=400
            )
        db.delete(role)
        db.commit()
        return True


# check if role and permissions exists
def check_permission(db: Session, role_id: int, permission_id: int) -> bool:
    has_perm = (
        db.query(models.RolePermissions)
        .filter(
            models.RolePermissions.permission == permission_id,
            models.RolePermissions.role == role_id,
        )
        .first()
    )
    if not has_perm:
        return False
    return True


def remove_role_permission(db: Session):
    db.query(models.RolePermissions).delete()
    db.commit()
