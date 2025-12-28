from sqlalchemy import Column, Integer, String,ForeignKey, Boolean, TIMESTAMP, text, DateTime
from ..database import Base
from sqlalchemy.orm import relationship
from cuid2 import Cuid
import datetime


cuid = Cuid()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    is_verifide = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    role = Column(String, nullable=False)
    
    
    moods = relationship("Mood", back_populates="user")
    


class PasswordResetCode(Base):
    __tablename__ = "password_reset_codes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    otp = Column(String(4), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    used = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    