from fastapi.exceptions import HTTPException
from fastapi.openapi.models import Schema
from sqlalchemy.orm.strategy_options import joinedload
from sqlalchemy.orm import Session

from todo import models


def get_todo(db: Session):
    todo_list = db.query(models.Task).filter(models.Task.is_deleted == False)
    return todo_list
