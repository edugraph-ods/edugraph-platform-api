from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

"""
UserModel is a class that represents a user in the database.

Attributes:
    id: The user's ID.
    email: The user's email.
    hashed_password: The user's hashed password.
    full_name: The user's full name.
    is_active: Whether the user is active.
    created_at: The date and time the user was created.
    updated_at: The date and time the user was last updated.
"""
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=True)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)