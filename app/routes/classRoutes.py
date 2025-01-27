""" Class and Meeting management by Teacher and Student

- create class
- show class
- create metting
- show meeting
"""

from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
# Cutom Models

from app.models.models import User,Class,Meeting
from app.database.db import get_db
from app.core.utilities import get_login_user
from app.schemas.classSchema import CreateClassRequest,CreateMeetingRequest



class_rout = APIRouter()


@class_rout.post("/create_class")
async def create_class(request:CreateClassRequest,
                        user:User= Depends(get_login_user),
                        db:AsyncSession=Depends(get_db)):
    try:
        new_class = await Class.create_class(
            teacher_id=user.id,
            subject=request.subject,
            start_time=request.start_time,
            end_time=request.end_time,
            )
        db.add(new_class)
        await db.commit()
        await db.refresh(new_class)
        return {"message": "Class created successfully", "class_id": new_class.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@class_rout.post("/book_meeting")
async def book_meeting(
    request:CreateMeetingRequest,
    user:User= Depends(get_login_user),
    db: AsyncSession = Depends(get_db)
):
    try:
        new_meeting = await Meeting.book_meeting(
            class_id=request.class_id, 
            student_id=user.id, 
            start_time=request.start_time, end_time=request.end_time, db=db)
        return {"message": "Meeting booked successfully", "meeting_id": new_meeting.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))



@class_rout.get("/my_classroom", status_code=status.HTTP_200_OK)
async def my_classroom(user:User= Depends(get_login_user),db:AsyncSession=Depends(get_db)):
    return await user.get_class_and_meeting_info(db)


@class_rout.get("/all_classroom", status_code=status.HTTP_200_OK)
async def all_classroom(db:AsyncSession=Depends(get_db)):
    query = select(Class)
    result = await db.execute(query)
    all_classrooms = result.scalars().all()
    return all_classrooms