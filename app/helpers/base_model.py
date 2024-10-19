from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, func

from typing_extensions import Dict, Any
from manager import Base


class BaseModel(Base):

    __abstract__ = True

    id = Column(Integer, primary_key=True)
    uid = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    created_by = Column(String, nullable=False, default="")

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        instance = cls()
        for key, value in data.items():
            setattr(instance, key, value)
        return instance
