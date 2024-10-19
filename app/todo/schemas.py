from datetime import datetime
from typing import Literal
from typing_extensions import Optional
from pydantic import BaseModel, Field
from fastapi import Query

from todo.constant import TaskStatus


# permission and role DTO
class TaskTypeBase(BaseModel):
    uid: str

    class Config:
        from_attributes = True


class TaskTypeCreate(BaseModel):
    name: str = Query(...)
    is_active: bool = Query(default=False)
    owner: Optional[int] = Field(None, exclude=True)


# for list and detail of projects
class TaskTypeDetail(TaskTypeBase):
    name: str
    status: str
    is_active: bool


# task DTO
class TaskBase(BaseModel):
    uid: str
    name: str
    is_active: bool

    class Config:
        from_attributes = True


class TaskCreateForm(BaseModel):
    name: str
    details: str = ""
    status: Literal[TaskStatus.pending, TaskStatus.completed]
    is_active: bool = True
    tasktype_id: str
    start_datetime: str
    end_datetime: str = ""
    is_everyday: bool = False


class TaskDetail(TaskBase):
    details: str
    status: str
    start_datetime: datetime
    end_datetime: datetime

    class Config:
        from_attributes = True
