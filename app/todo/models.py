from helpers.base_model import BaseModel
from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    func,
    Date,
    Time,
)
from sqlalchemy.orm import relationship

from todo.constant import ProjectStatus, TaskStatus
from datetime import datetime


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
    start_date = Column(Date, nullable=False, server_default=func.now())
    end_date = Column(Date, nullable=True)
    start_time = Column(Time, nullable=False, server_default=func.now())
    end_time = Column(Time, nullable=False, server_default=func.now())
    is_everyday = Column(Boolean, default=False)
    exclude_days = Column(String, nullable=False, default="")

    # relationship
    task_type = relationship("TaskType", back_populates="task")
