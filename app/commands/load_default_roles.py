from sqlalchemy.orm import Session

from auth import schemas
from services.role_perm import create_role, get_role_by_name
from manager.database import get_db


def load_default_roles():
    db: Session = next(get_db())
    role_name = input("enter role name: ")
    role = schemas.CreateRole(**{"name": role_name.lower(), "is_active": True})
    role_instance = get_role_by_name(db=db, role_name=role_name.lower())
    if role_instance:
        print(f"role already exists with name {role_name}")
        return
    create_role(db=db, role=role)
    print("role created successfully")
