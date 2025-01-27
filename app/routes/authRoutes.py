""" User Authentication APIs

- login
- registartion
"""

from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

# Cutom Models
from app.schemas.authSchema import LoginRequest,RegistrationRequest
from app.models.models import User
from app.database.db import get_db
from app.core.utilities import create_access_token,get_login_user
auth_rout = APIRouter()

@auth_rout.post("/registration",status_code=status.HTTP_200_OK)
async def registration(request:RegistrationRequest,db: AsyncSession = Depends(get_db)):
    try:
        user = User.create_user(**request.model_dump())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return JSONResponse(
            content={"message": "User created successfully"},
            status_code=status.HTTP_201_CREATED
        )
    except Exception as e:
        return JSONResponse(
            content={"message": f"Something went wrong: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    


    
@auth_rout.post("/login", status_code=status.HTTP_200_OK)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    try:
        user = await User.user_get_by_email(request.email, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found!")
        if not user.verify_password(request.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password!")
        
        #  Create Access token
        token = create_access_token(data={"email":user.email})
        return JSONResponse(
            content={"message": "Login successful", 
                    "user": user.email,
                    "token":token
                    },
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"message": f"Something went wrong: {str(e)}"},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@auth_rout.post("/recreate_token", status_code=status.HTTP_200_OK)
async def recreate_token(user:User= Depends(get_login_user)):
    token = create_access_token(data={"email":user.email})
    return JSONResponse(
            content={"message": "generate new Token successful", 
                    "user": user.email,
                    "token":token
                    },
            status_code=status.HTTP_200_OK
        )