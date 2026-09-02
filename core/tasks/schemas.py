from pydantic import Field, BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class TaskBaseSchema(BaseModel):
    title: str = Field(..., max_length=150, description="title of the task")
    description: Optional[str] = Field(None, max_length=500, description="description of the task")
    is_completed: bool = Field(..., description="the current state of the task")


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskReturnSchema(TaskBaseSchema):
    id: UUID = Field(..., description="unique identifier of the task")
    created_date: datetime = Field(..., description="timestamp when the task was created")
    updated_date: datetime = Field(..., description="timestamp when the task was last updated")
    
   