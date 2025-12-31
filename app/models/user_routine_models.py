from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, JSON, Boolean, TIMESTAMP, text
from sqlalchemy.orm import relationship
from ..database import Base



class Routine(Base):
    __tablename__ = "routines"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String, nullable=False)
    duration_minutes = Column(Integer, default=30)
    is_ai_generated = Column(Boolean, default=False)
    scheduled_time = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    user = relationship("User", back_populates="routines")
    activities = relationship("RoutineActivity", back_populates="routine", cascade="all, delete-orphan")



class RoutineActivity(Base):
    __tablename__ = "routine_activities"
    
    id = Column(Integer, primary_key=True, index=True)
    routine_id = Column(Integer, ForeignKey("routines.id", ondelete="CASCADE"))
    activity_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    content_id = Column(String, nullable=True)
    
    routine = relationship("Routine", back_populates="activities")