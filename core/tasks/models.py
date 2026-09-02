from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.types import Uuid

from core.database import Base




class TaskModel(Base):
    __tablename__ = "tasks"
    id = Column(Uuid, primary_key=True, default=uuid4, autoincrement=True)
    title = Column(String(150), nullable=False)
    description = Column(String(150), nullable=False)
    is_compeleted = Column(Boolean, default=False)
    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), server_onupdate=func.now())


