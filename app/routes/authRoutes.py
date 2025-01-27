""" User Authentication APIs

- login
- registartion
"""

from fastapi import APIRouter

# Cutom Models
from app.schemas.authSchema import LoginRequest,RegistrationRequest




auth_rout = APIRouter()

@auth_rout.post("/registration")
async def registration(request:RegistrationRequest):
    return request

@auth_rout.post("/login")
async def login(request:LoginRequest):
    return request
