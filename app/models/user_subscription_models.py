from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base




class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    plan = Column(String, nullable=False)
    status = Column(String, default="active")
    started_at = Column(DateTime, default= datetime.utcnow)
    ends_at = Column(DateTime, nullable=True)
    payment_provider = Column(String, nullable=True)
    payment_id = Column(String, nullable=True)
    payload_provider = Column(String)
    
    @property
    def is_active(self) -> bool:
        return self.status == "active"
    
    user = relationship("User", back_populates="subscription")