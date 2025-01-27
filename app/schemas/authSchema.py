""" Schema for Authentication

- LoginRequest
- RegistrationRequest
"""

from pydantic import BaseModel, field_validator,EmailStr

# Cutom Modules
from app.models.models import Role

class RegistrationRequest(BaseModel):
    first_name: str = "Jay"
    last_name: str = "Patel"
    email:EmailStr = "jay@gmail.com"
    phone: str = "7069668308"
    age:float = 24
    role:Role = Role.TEACHER
    password: str = "123456"

    @field_validator("phone")
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
    email: str = "jay@gmail.com"
    password: str = "123456"

    @field_validator("password")
    def validate_password(cls, password: str):
        print("Password used by validator:", password)
        if len(password) < 6:
            raise ValueError("Password must be 6 characters long")
        return password

