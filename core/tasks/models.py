# tasks/models.py
from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, String, Integer, func, ForeignKey
from sqlalchemy.types import Uuid
from core.database import Base
from sqlalchemy.orm import relationship

class TaskModel(Base):
    __tablename__ = "tasks"
    
    id = Column(Uuid, primary_key=True, default=uuid4)
    title = Column(String(150), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    description = Column(String(500), nullable=True)
    is_completed = Column(Boolean, default=False) 
    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), onupdate=func.now())
    user = relationship("UserModel", back_populates="tasks")