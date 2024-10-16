
from pydantic import BaseModel, EmailStr,Field
from sqlalchemy.sql.base import Options
from sqlalchemy.sql.operators import regexp_match_op
from sqlalchemy.sql.sqltypes import BOOLEAN
from typing import List,Optional
from typing_extensions import Annotated
from helpers.decorators import validate_password
from auth import models

#permission and role DTO
class ProjectBase(BaseModel):
    uid:str

class ProjectCreate(BaseModel):
    name: str
    status: str
    is_active: bool
    owner:int
    class Config:
           from_attributes=True

#for list and detail of projects
class ProjectDetail(ProjectBase):
    name:str
    status: str
    is_active: bool


#task DTO
class TaskBase(BaseModel):
    uid:str
    name:str
    is_active:bool

class TaskCreate(BaseModel):
    name:str
    detail:str
    status:str
    is_active:bool
    project_id: str

class TaskDetail(TaskBase):
    detail:str
    status:str
    project:ProjectBase
