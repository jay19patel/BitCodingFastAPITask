from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str =  "postgresql+asyncpg://postgres:admin@postgres/class_booking_system"
    SECRET_KEY:str = "very-secret-key-is-jay"
    ALGORITHM:str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 15

setting = Settings()