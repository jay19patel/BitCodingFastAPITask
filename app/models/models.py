"""
Managing all models:

- Role
- Subjects
- User Model:
    - hash_password
    - verify_password
    - create_user
"""

from sqlalchemy import Column, String, Integer, DateTime, func, Enum as sqlEnum, ForeignKey,Boolean,Time,select
from sqlalchemy.orm import relationship, validates
from enum import Enum
from passlib.context import CryptContext
from datetime import datetime
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
# Custom modules
from app.database.db import Base,get_db 
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

# User model
class User(Base):
    """User model
    - hash_password
    - verify_password
    - create_user
    - user_get_by_email
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
    classes = relationship("Class", back_populates="teacher")  # One teacher user has multiple classes
    meetings = relationship("Meeting", back_populates="student")  # One student can have multiple meetings

    @classmethod
    def hash_password(cls, password: str) -> str:
        """Hash the password."""
        return pwd_context.hash(password)

    def verify_password(self, password: str) -> bool:
        """Verify the password."""
        return pwd_context.verify(password, self.password)

    @classmethod
    def create_user(cls, first_name: str, last_name: str, email: str, phone: str, age: float, password: str, role: Role = Role.STUDENT):
        """Create a new user with password security."""
        hashed_password = cls.hash_password(password)
        user = cls(first_name=first_name, last_name=last_name, email=email, phone=phone, password=hashed_password, role=role)
        return user

    @classmethod
    async def user_get_by_email(cls, email: EmailStr, db: AsyncSession):
        """Find user by email ID."""
        query = select(cls).where(cls.email == email)
        result = await db.execute(query)
        if not result:
            return False
        return result.scalars().first()

    async def get_class_and_meeting_info(self, db: AsyncSession):
        """Get the number of classes created by the user and the number of students scheduled for meetings."""
        # Get all classes created by the user
        query = select(Class).where(Class.teacher_id == self.id)
        result = await db.execute(query)
        classes = result.scalars().all()

        class_count = len(classes)
        student_meetings_info = []

        for classroom in classes:
            # Get the students scheduled for this class
            query_meetings = select(Meeting).where(Meeting.class_id == classroom.id)
            result_meetings = await db.execute(query_meetings)
            meetings = result_meetings.scalars().all()

            student_count = len(meetings)
            meeting_times = [{"student":meeting.student_id,
                              "start_time":meeting.start_time, 
                              "end_time":meeting.end_time} for meeting in meetings]

            student_meetings_info.append({
                "class_id": classroom.id,
                "subject": classroom.subject,
                "start_time":classroom.start_time,
                "end_time":classroom.end_time,
                "student_count": student_count,
                "meeting_times": meeting_times,
            })

        return {
            "class_count": class_count,
            "student_meetings_info": student_meetings_info
        }
    

class Class(Base):
    """Class model to store class information set by a teacher"""
    __tablename__ = "classes"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_id = Column(Integer, ForeignKey("users.id"))
    subject = Column(sqlEnum(Subjects), default=Subjects.ENGLISH, nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    teacher = relationship("User", back_populates="classes")
    meetings = relationship("Meeting", back_populates="class_")

    @classmethod
    async def create_class(cls, teacher_id: int, subject: Subjects, start_time: datetime, end_time: datetime):
        if start_time >= end_time:
            raise ValueError("Start time must be before end time.")
        return cls(teacher_id=teacher_id, subject=subject, start_time=start_time, end_time=end_time)
    

class Meeting(Base):
    """Meeting model for student to book meeting slots in a class"""
    __tablename__ = "meetings"
    
    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"))
    student_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    created_datetime = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    # Relationships
    class_ = relationship("Class", back_populates="meetings")
    student = relationship("User", back_populates="meetings")

    @classmethod
    async def book_meeting(cls, class_id: int, student_id: int, start_time: datetime, end_time: datetime, db: AsyncSession):
        query = select(cls).where(cls.class_id == class_id)
        result = await db.execute(query)
        meetings = result.scalars().all()
        
        for meeting in meetings:
            if (start_time < meeting.end_time and end_time > meeting.start_time):
                raise ValueError("The selected time slot is already booked.")
        
        new_meeting = cls(class_id=class_id, student_id=student_id, start_time=start_time, end_time=end_time)
        db.add(new_meeting)
        await db.commit()
        return new_meeting
