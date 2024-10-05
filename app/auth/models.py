import shortuuid
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from manager import Base
from helpers.base_model import BaseModel

class UserRole(Base):
    __tablename__ = 'user_role'

    user=Column('user_id', ForeignKey('user.id'), primary_key=True)
    role=Column('role_id', ForeignKey('role.id'), primary_key=True)


class User(BaseModel):
    __tablename__ = 'user'

    id= Column(Integer, primary_key=True)
    uid=Column(String,unique=True,index=True)
    username= Column(String,unique=True,nullable=True, default="")
    email= Column(String, unique=True, index=True)
    password=Column(String,default="")
    pasword_salt= Column(String)
    is_superuser=Column(Boolean,default=False)
    is_active= Column(Boolean, default=True)
    is_verified=Column(Boolean, default=False)
    first_name= Column(String,default="")
    last_name= Column(String,default="")
    number = Column(String)
    age= Column(Integer)
    address= Column(String, nullable=False,default="")
    role= relationship("Roles",secondary="user_role",back_populates="user")

class RolePermissions(Base):
    __tablename__= 'role_permission'

    role=Column('role_id',ForeignKey('role.id'),primary_key=True)
    permission=Column('permission_id',ForeignKey('permission.id'),primary_key=True)


class Roles(BaseModel):
    __tablename__="role"

    id=Column(Integer, primary_key=True)
    uid=Column(String, unique=True,index=True)
    name=Column(String,unique=True)
    is_active=Column(Boolean,default=True)
    user=relationship("User",secondary="user_role",back_populates="role")
    permission=relationship("Permissions",secondary="role_permission",back_populates="role")


class Permissions(Base):
    __tablename__="permission"

    id= Column(Integer, primary_key=True,index=True)
    url_path= Column(String,index=True)
    method= Column(String,default="")
    name= Column(String,default="")
    uid= Column(String,index=True,nullable=False,default="")
    role= relationship("Roles",secondary="role_permission",back_populates="permission")
