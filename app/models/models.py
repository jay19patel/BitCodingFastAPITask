"""
Managing all models:

- Role
- Subjects
- User Model:
    - hash_password
    - verify_password
    - create_user
"""

from sqlalchemy import Column, String, Integer, DateTime, func, Enum as sqlEnum, ForeignKey,Boolean,Time
from sqlalchemy.orm import relationship, validates
from enum import Enum
from passlib.context import CryptContext
from datetime import datetime

# Custom modules
from app.database.db import Base

class Role(Enum):
    """User roles"""
    STUDENT = 'Student'
    TEACHER = 'Teacher'

class Subjects(Enum):
    """Subjects for Teachers"""
    MATH = "Mathematics"
    SCIENCE = "Science"
    HISTORY = "History"
    ENGLISH = "English"
    GEOGRAPHY = "Geography"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """User model
    - hash_password
    - verify_password
    - create_user
    """
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False, index=True)
    phone = Column(String(15), nullable=True, unique=True)
    age = Column(Integer, nullable=True)
    password = Column(String, nullable=False)
    role = Column(sqlEnum(Role), default=Role.STUDENT, nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    classes = relationship("Classroom", back_populates="users")

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash the password."""
        return pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify the password."""
        return pwd_context.verify(password, self.password)

    @classmethod
    def create_user(cls, first_name: str, last_name: str, email: str, password: str, role: Role = Role.STUDENT):
        """Create a new user with password security."""
        hashed_password = cls.hash_password(password)
        user = cls(first_name=first_name, last_name=last_name, email=email, password=hashed_password, role=role)
        return user
