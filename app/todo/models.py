from helpers.base_model import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from todo.constant import ProjectStatus, TaskStatus

class Project(BaseModel):
    __tablename__='project'

    name= Column(String(length=255), nullable=False, default="")
    status= Column(String, nullable=False, default=ProjectStatus.pending)
    owner= Column(Integer, ForeignKey('user.id'), nullable=False)
    #relationship
    project= relationship("Task", back_populates="project")


class Task(BaseModel):
    __tablename__= "task"

    name= Column(String, nullable=False, default="")
    details= Column(String, nullable=False, default="")
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    assign_to_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    status= Column(String, nullable=False,default=TaskStatus.pending)
    #relationship
    sub_tasks= relationship("SubTask", back_populates="task")
    project = relationship("Project", back_populates="project")


class SubTask(BaseModel):
    __tablename__= "subtask"

    name= Column(String(length=255), nullable=False)
    details= Column(String, nullable=False, default="")
    task_id= Column(Integer, ForeignKey('task.id'), nullable=True)
    status= Column(String, nullable=False, default=TaskStatus.pending)
    #relationship
    task= relationship("Task", back_populates="sub_tasks")

