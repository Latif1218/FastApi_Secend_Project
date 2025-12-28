from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from ..database import Base



class Habit(Base):
    __tablename__ = "user_habits"
    
    id = Column(Integer, primary_key=True, index= True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=False)
    frequency = Column(String, default="daily")
    reminder_time = Column(String, nullable=True)
    streak = Column(Integer, default=0)
    completed_dates = Column(JSON, default=list)
    
    
    user = relationship("User", back_populates="habits")