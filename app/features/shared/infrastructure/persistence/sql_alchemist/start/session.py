import ssl

from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.core.config.config import settings


# Azure MySQL Flexible Server
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

engine = create_async_engine(settings.database_url, future=True, echo=False, connect_args={"ssl": ssl_context})
async_session_maker = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

"""
create_database_if_not_exists is a function that creates a database if it does not exist.
"""
async def create_database_if_not_exists():
    url = make_url(settings.database_url)
    database = url.database
    if not database:
        return

    server_db = "mysql"
    server_url = url.set(database=server_db)
    temp_engine = create_async_engine(server_url, future=True, echo=False, connect_args={"ssl": ssl_context})

    async with temp_engine.begin() as conn:
        await conn.execute(
            text(
                f"CREATE DATABASE IF NOT EXISTS `{database}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
            )
        )

    await temp_engine.dispose()


"""
get_db is a function that returns a database session.

Returns:
    AsyncSession: The database session.
"""
async def get_db():
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()