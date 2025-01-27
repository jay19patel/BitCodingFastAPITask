""" FastAPI main app
"""

from fastapi import FastAPI
from contextlib import asynccontextmanager

# Custom Modules
from app.database.db import init_db
from app.routes.authRoutes import auth_rout
@asynccontextmanager
async def connectingTodb(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="Online Class Booking",
    version="1.0.0", 
    summary="Create an Online Class Booking system where students can easily connect with teachers.",
    lifespan=connectingTodb
)


app.include_router(auth_rout,prefix="/auth",tags=["User Login and Registartion"])