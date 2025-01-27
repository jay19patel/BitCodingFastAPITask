""" Schema for Class And Meetings

- Create Class
- Create Meeting
"""

from pydantic import BaseModel, field_validator,EmailStr
from datetime import datetime,timedelta
# Cutom Modules
from app.models.models import Subjects

class CreateClassRequest(BaseModel):
    subject: Subjects = Subjects.MATH
    start_time:datetime = datetime.now()
    end_time:datetime = datetime.now()+ timedelta(hours=5)

class CreateMeetingRequest(BaseModel):
    class_id: int = 3
    start_time:datetime = datetime.now()
    end_time:datetime = datetime.now()+ timedelta(hours=1)