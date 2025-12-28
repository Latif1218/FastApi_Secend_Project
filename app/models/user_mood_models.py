from sqlalchemy import Column, Integer, ForeignKey, JSON, TIMESTAMP, String, text
from sqlalchemy.orm import relationship
from ..database import Base



class Mood(Base):
    __tablename__ = "user_moods"
    
    id = Column(Integer, primary_key=True, index= True)
    user_id = Column(Integer, ForeignKey("users.id"))
    rating = Column(Integer, nullable=False)
    emotions = Column(JSON, nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    
    user = relationship("User", back_populates="moods")