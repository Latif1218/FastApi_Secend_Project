from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

class FrequencyEnum(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"
    
    
class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: str
    frequency: FrequencyEnum = FrequencyEnum.daily
    reminder_time: Optional[str] = None
    
    
class HabitCreate(HabitBase):
    pass


class HabitUpdate(HabitBase):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    frequency: Optional[str] = None
    reminder_time: Optional[str] = None
    
    
class HabitOut(HabitBase):
    id: int
    streak: int 
    completed_dates: List[str] 
    
    class Config:
        from_attributes = True
        