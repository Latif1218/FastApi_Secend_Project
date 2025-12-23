from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text, DateTime
from .. database import Base



class User(Base):
    __tabkename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    is_verifide = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    role = Column(String, nullable=False)
    
    
