from fastapi import Depends
from sqlalchemy.orm.session import Session
from manager.database import get_db

def create_superuser():
    db:Session=next(get_db())
    email= input("email: ")
    password= input("password: ")
    confirm_password= input("confirm password: ")
