"""" PostgreSQL
Connectiong with PostgreSQL using SQLAlchemy

- Base
- init_db
- get_db

"""



from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import setting


engine = create_async_engine(setting.DATABASE_URL)

Base = declarative_base()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db():
    async with async_session() as session:
        yield session