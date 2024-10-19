from datetime import date, time
from typing import Literal
from typing_extensions import Optional, Union
from pydantic import BaseModel, Field
from fastapi import Query, Form

from todo.constant import TaskStatus


# permission and role DTO
class TaskTypeBase(BaseModel):
    uid: str

    class Config:
        from_attributes = True


class TaskTypeCreate(BaseModel):
    name: str
    is_active: bool = True
    owner: Optional[int] = 0


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
    start_date: str
    end_date: str = ""
    start_time: str
    end_time: str = ""
    is_everyday: bool = False
    exclude_days: str = ""


class TaskDetail(TaskBase):
    details: str
    status: str
    start_date: Union[date, None]
    end_date: Union[date, None]
    start_time: Union[time, None]
    end_time: Union[time, None]
    is_everyday: bool
    exclude_days: str

    class Config:
        from_attributes = True
