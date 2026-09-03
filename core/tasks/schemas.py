from pydantic import Field, BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID

class TaskBaseSchema(BaseModel):
    title: str = Field(..., max_length=150, description="title of the task")
    description: Optional[str] = Field(None, max_length=500, description="description of the task")
    is_completed: bool = Field(default=False, description="the current state of the task")

class TaskCreateSchema(TaskBaseSchema):
    pass

class TaskUpdateSchema(TaskBaseSchema):
    # Make fields optional for updates
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

class TaskReturnSchema(TaskBaseSchema):
    id: UUID = Field(..., description="unique identifier of the task")
    user_id: int = Field(..., description="ID of the user who owns this task") # Added this
    created_date: datetime = Field(..., description="timestamp when the task was created")
    updated_date: datetime = Field(..., description="timestamp when the task was last updated")

    model_config = {
        "from_attributes": True
    }