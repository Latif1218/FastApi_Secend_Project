from pydantic import BaseModel
from typing import List
from datetime import datetime


class MoodCreate(BaseModel):
    rating: int
    emotions: List[str]
    note: str | None = None
    

class MoodOut(BaseModel):
    id: int
    rating: int
    emotions: List[str]
    note: str | None
    created_at: datetime
    
    class Config: 
        from_attributes = True