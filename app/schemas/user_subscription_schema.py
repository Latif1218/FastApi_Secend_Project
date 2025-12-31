from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class PlanEnum(str, Enum):
    free = "free"
    monthly = "monthly"
    yearly = "yearly"


class SubscriptionBase(BaseModel):
    plan: PlanEnum = PlanEnum.free
    
    
class PProEnum(str, Enum):
    stripe = "stripe"
    apple = "apple"
    google = "google"
    
    
class SubscriptionCreate(SubscriptionBase):
    payment_id: Optional[str] = None
    payment_provider: PProEnum = PProEnum.stripe
    
    
    
class StatusEnum(str, Enum):
    active = "active"
    canceled = "canceled"
    expired = "expired"
    
    
class SubscriptionOut(SubscriptionBase):
    id: Optional[int] = None 
    plan: str
    status: StatusEnum = StatusEnum.active
    started_at: datetime
    ends_at: Optional[datetime]
    is_active: bool 
    
    class Config:
        from_attributes = True