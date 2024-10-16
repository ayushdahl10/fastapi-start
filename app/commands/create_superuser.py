from fastapi import Depends
from pydantic_core.core_schema import ErrorType
import shortuuid
from sqlalchemy.orm.session import Session
import getpass

from manager.database import get_db
from services import auth_service
from auth import schemas, models
from helpers.auth_helper import hash_password

def create_superuser():
    db: Session = next(get_db())
    
    email = input("Email: ")
    password = getpass.getpass("Password: ")
    confirm_password = getpass.getpass("Confirm Password: ")

    if password != confirm_password:
        raise Exception("Passwords don't match")

    hashed_password = hash_password(password)

    db_user = models.User(
        email=email,
        password=hashed_password,
        uid=shortuuid.uuid(),
        first_name="",
        last_name="",
        age=0,
        username=email,
        is_superuser=True,
        is_verified=True,
    )

    db.add(db_user)
    db.commit()
    print("Superuser created successfully")

