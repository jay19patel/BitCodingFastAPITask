""" Schema for Authentication

- LoginRequest
- RegistrationRequest
"""

from pydantic import BaseModel, field_validator,EmailStr

# Cutom Modules
from app.models.models import Role

class RegistrationRequest(BaseModel):
    first_name: str
    last_name: str
    email:EmailStr
    phone_number: str
    age:float
    role:Role
    password: str

    @field_validator("phone_number")
    def validate_phone_number(cls, phone_number: str):
        print("Validated phone number:", phone_number)
        if len(phone_number) != 10:
            raise ValueError("Phone number is not valid!")
        return phone_number
    
    @field_validator("password")
    def validate_password(cls, password: str):
        if len(password) < 6:
            raise ValueError("Password must be 6 characters long")
        return password


class LoginRequest(BaseModel):
    username: str
    password: str

    @field_validator("password")
    def validate_password(cls, password: str):
        print("Password used by validator:", password)
        if len(password) < 6:
            raise ValueError("Password must be 6 characters long")
        return password

