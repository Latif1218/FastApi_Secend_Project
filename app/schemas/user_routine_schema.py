from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime



class RoutineActivityBase(BaseModel):
    activity_type: str
    title: str
    duration_minutes: int
    content_id: Optional[str] = None
    
    
class RoutineActivityCreate(RoutineActivityBase):
    pass    


class RoutineActivityOut(RoutineActivityBase):
    id: int
    
    class Config:
        from_attributes = True
        
        
class RoutineBase(BaseModel):
    name: str
    duration_minutes: Optional[int] = 30
    is_ai_generated: bool = False
    scheduled_time: Optional[str] = None
    
    
class RoutineCreate(RoutineBase):
    activities: List[RoutineActivityCreate]
    
    
class RoutineUpdate(RoutineBase):
    name: Optional[str] = None
    duration_minutes: Optional[int] = None
    scheduled_time: Optional[str] = None
    activities: Optional[List[RoutineActivityCreate]]= None
    
    
    
class RoutineOut(RoutineBase):
    id: int
    completed: bool = False
    completed_at: Optional[datetime] = None
    created_at: datetime
    activities: List[RoutineActivityOut] = []
    
    class Config:
        from_attributes = True
        