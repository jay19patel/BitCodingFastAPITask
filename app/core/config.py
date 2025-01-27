from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str =  "postgresql+asyncpg://postgres:admin@localhost:5432/OnlineClassBooking"

setting = Settings()