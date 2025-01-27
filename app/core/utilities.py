""" Utilities for JWT and Authentication 
- AccessTokenBearer
- create_access_token
- decode_access_token
- recreate_access_token
- get_login_user
"""


from datetime import datetime,timedelta,timezone
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends,Request,HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials


# Cutom Modules
from app.core.config import setting
from app.database.db import get_db
from sqlalchemy import select
from app.models.models import User
class AccessTokenBearer(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        if not self.token_valid(token):
            raise HTTPException(
                detail="Access token is invalid or expired.",
                status_code=status.HTTP_403_FORBIDDEN
            )

        token_data = decode_access_token(token)

        if datetime.fromtimestamp(token_data["exp"]) < datetime.now():
            raise HTTPException(
                detail="Access token has expired.",
                status_code=status.HTTP_403_FORBIDDEN
            )
        return token_data

    def token_valid(self, token: str) -> bool:
        try:
            token_data = decode_access_token(token)
            return token_data is not None
        except:
            return False
        

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, setting.SECRET_KEY, algorithm=setting.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, setting.SECRET_KEY, algorithms=[setting.ALGORITHM])
        return payload
    except InvalidTokenError as e:
        return None

def recreate_access_token(token:str):
    email_row = decode_access_token(token)
    if email_row.get("email"):
        new_token = create_access_token(data={"email":email_row.get("email")})
        return new_token
    else:
        raise HTTPException(detail="Something wrong to recreating access token",
                            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
async def get_login_user(request: dict = Depends(AccessTokenBearer()), db: AsyncSession = Depends(get_db)):
    try:
        user = await User.user_get_by_email(request.get("email"),db)
        return user
    except:
        return False