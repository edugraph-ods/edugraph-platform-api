from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.features.authentication.infrastructure.persistence.sql_alchemist.models.user_model import Base
from app.shared.infrastructure.persistence.sql_alchemist.session import create_database_if_not_exists, engine

from app.features.authentication.interfaces.rest.routers.auth_router import router as auth_router
from app.features.education.interfaces.rest.controller.ingest_router import router as ingest_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database_if_not_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="QuickStore API",
    description="The RESTAPI application documentation for QuickStore",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

app.include_router(auth_router)
app.include_router(ingest_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
