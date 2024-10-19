from helpers.base_model import BaseModel
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func
from sqlalchemy.orm import relationship

from todo.constant import ProjectStatus, TaskStatus


# task_type
class TaskType(BaseModel):
    __tablename__ = "tasktype"

    name = Column(String(length=255), nullable=False, default="", unique=True)
    status = Column(String, nullable=False, default=ProjectStatus.in_progress)
    owner = Column(Integer, ForeignKey("user.id"), nullable=True)
    is_default = Column(Boolean, default=False, nullable=False)
    # relationship
    task = relationship("Task", back_populates="task_type")


class Task(BaseModel):
    __tablename__ = "task"

    name = Column(String, nullable=False, default="")
    details = Column(String, nullable=False, default="")
    tasktype_id = Column(Integer, ForeignKey("tasktype.id"), nullable=False)
    status = Column(String, nullable=False, default=TaskStatus.pending)
    start_datetime = Column(DateTime, nullable=False, server_default=func.now())
    end_datetime = Column(DateTime, nullable=True)
    is_everyday = Column(Boolean, default=False)

    # relationship
    task_type = relationship("TaskType", back_populates="task")
