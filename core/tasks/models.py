# tasks/models.py
from uuid import uuid4
from sqlalchemy import Boolean, Column, DateTime, String, func
from sqlalchemy.types import Uuid
from core.database import Base

class TaskModel(Base):
    __tablename__ = "tasks" # Also fixed: added double underscores
    
    id = Column(Uuid, primary_key=True, default=uuid4)
    title = Column(String(150), nullable=False)
    description = Column(String(500), nullable=True) # Fixed: max length should match schema
    is_completed = Column(Boolean, default=False) # FIXED: was 'is_compeleted'
    created_date = Column(DateTime, server_default=func.now())
    updated_date = Column(DateTime, server_default=func.now(), onupdate=func.now())