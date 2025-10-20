from typing import Union

from fastapi import FastAPI

from app.api.v1.routers.auth_router import router as auth_router
from app.api.v1.routers.protected_router import router as protected_router
from app.api.v1.routers.ingest_router import router as ingest_router
from app.adapters.db.models import Base
from app.adapters.db.session import create_database_if_not_exists, engine

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await create_database_if_not_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.include_router(auth_router)
app.include_router(ingest_router)

