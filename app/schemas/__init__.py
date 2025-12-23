from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime




class UserCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128, description="password must be between 8 to 128 characters")
    role: str = "user"
    
    @field_validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v 
    
class UserRespons(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orrm_model = True 