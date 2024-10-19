from pydantic import BaseModel, EmailStr, Field
from pydantic.types import Strict
from sqlalchemy.sql.base import Options
from sqlalchemy.sql.operators import regexp_match_op
from sqlalchemy.sql.sqltypes import BOOLEAN
from typing import List, Optional
from typing_extensions import Annotated


from helpers.decorators import validate_password
from auth import models


# permission and role DTO
class RoleBase(BaseModel):
    name: str


class Role(RoleBase):
    uid: str
    is_active: bool

    class Config:
        from_attributes = True


class PermissionBase(BaseModel):
    id: str


class RoleDetail(Role):
    permission: List[PermissionBase]


class Permission(BaseModel):
    url_path: str
    name: str
    method: str

    class Config:
        from_attributes = True


class CreateRole(RoleBase):
    is_active: bool


class CreateRolePermissions(RoleBase):
    permissions: List[PermissionBase]


# user DTO
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(min_length=8)
    first_name: str
    last_name: str
    age: int = Field(gt=18)
    is_active: bool = True


class UserUpdate(UserBase):
    first_name: str
    last_name: str
    age: int = Field(gt=18)
    is_active: bool


class User(UserBase):
    first_name: str
    last_name: str
    id: int
    is_active: bool
    uid: str
    age: int
    role: List[Role]

    class Config:
        from_attributes = True


class UserAdmin(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    age: int = Field(gt=18)
    is_active: bool
    roles: list

    class Config:
        from_attribute = True


class UserLogin(BaseModel):
    email: str
    password: str


class RegisterUser(UserBase):
    password: str
    confirm_password: str
    first_name: str
    last_name: str
    age: int = Field(gt=12)
