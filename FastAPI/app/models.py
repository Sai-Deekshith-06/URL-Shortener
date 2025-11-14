# SQLalchemy models
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    is_active = Column(Boolean, default=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    # When you access user.urls, SQLAlchemy will actually go and 
    # fetch the items from the database in the urls table and populate them here.
    urls = relationship("URL", back_populates="owner")

class URL(Base):
    """
    id, long_url, owner_id, password, short_code, created_at, expires_at
    """
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(String, index=True, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    password = Column(String, nullable=True)
    short_code = Column(String, unique=True, nullable=False, index=True)
    created_at = Column(DateTime, default=func.now())
    expires_at = Column(DateTime, nullable=True)

    owner = relationship("User", back_populates="urls")