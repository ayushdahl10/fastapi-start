from fastapi import Depends
import shortuuid
from sqlalchemy.orm.session import Session

from manager.database import get_db
from services import auth_service
from auth import schemas,models
from helpers.auth_helper import hash_password


def create_superuser():
    db:Session=next(get_db())
    email= input("email: ")
    password= input("password: ")
    confirm_password= input("confirm password: ")
    password=hash_password(password)
    db_user= models.User(email=email, password=password,
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
    print("superuser created successfully")
