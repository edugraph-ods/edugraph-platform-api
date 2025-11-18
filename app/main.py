from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from contextlib import asynccontextmanager

from app.features.authentication.infrastructure.persistence.sql_alchemist.models.user_model import Base
import app.features.authentication.infrastructure.persistence.sql_alchemist.models.student_model
import app.features.education.infrastructure.persistence.sql_alchemist.models.university_model

from app.features.shared.infrastructure.persistence.sql_alchemist.session import create_database_if_not_exists, engine

from app.features.authentication.infrastructure.tokens.jwt.services.token_service_impl import TokenServiceImpl
from app.features.authentication.interfaces.rest.routers.auth_router import router as auth_router
from app.features.authentication.interfaces.rest.routers.users_router import router as users_router
from app.features.authentication.interfaces.rest.routers.students_router import router as students_router
from app.features.authentication.infrastructure.middleware.auth_middleware import AuthMiddleware

from app.core.config.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database_if_not_exists()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title="EduGraph API",
    description="The RESTAPI application documentation for EduGraph",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

token_service = TokenServiceImpl(
    secret_key=settings.secret_key,
    algorithm=settings.algorithm,
    access_token_expire_minutes=settings.access_token_expire_minutes,
)

app.add_middleware(
    AuthMiddleware,
    token_service=token_service,
    public_paths={
        "/api/v1/sign-up",
        "/api/v1/sign-in",
        "/api/v1/users/recovery-code",
        "/api/v1/users/verify-recovery-code",
        "/api/v1/users/reset-password",
    },
    public_prefixes=(),
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    components = openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})
    security_schemes["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    openapi_schema["security"] = [{"bearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(students_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
