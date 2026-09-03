from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class UserLoginSchema(BaseModel):
    username: str = Field(..., max_length=250, description="username of the user")
    password: str = Field(..., description="password of the user")

class UserRegisterSchema(BaseModel):
    username: str = Field(..., max_length=250, description="username of the user")
    password: str = Field(..., description="password of the user")
    # Note: Keeping your spelling 'conformation' to match your code, but 'confirmation' is standard English
    password_conformation: str = Field(..., description="password confirmation")

    @field_validator("password_conformation")
    @classmethod
    def passwords_match(cls, v, info):
        # 'info.data' contains the fields validated so far
        if 'password' in info.data and v != info.data['password']:
            raise ValueError('passwords do not match')
        return v

# Alias for clarity in routes
UserCreateSchema = UserRegisterSchema

class UserReturnSchema(BaseModel):
    id: int
    username: str
    is_active: bool
    created_date: Optional[datetime] = None
    
    model_config = {
        "from_attributes": True  # Allows Pydantic to read from SQLAlchemy objects
    }