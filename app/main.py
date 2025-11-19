import os

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from contextlib import asynccontextmanager

from app.features.authentication.users.infrastructure.persistence.sql_alchemist.models.user_model import Base
import app.features.authentication.students.infrastructure.persistence.sql_alchemist.models.student_model
import app.features.education.universities.infrastructure.persistence.sql_alchemist.models.university_model

from app.features.education.universities.application.internal.inbound_services.use_cases.create_university_use_case import (
    CreateUniversityUseCase,
)
from app.features.education.universities.infrastructure.loaders.csv.university_csv_loader import (
    UniversityCSVLoader,
)
from app.features.education.universities.infrastructure.persistence.sql_alchemist.repositories.university_repository_impl import (
    UniversityRepositoryImpl,
)

from app.features.shared.infrastructure.persistence.sql_alchemist.session import (
    create_database_if_not_exists,
    engine,
    async_session_maker,
)

from app.features.authentication.users.infrastructure.tokens.jwt.services.token_service_impl import (
    TokenServiceImpl,
)
from app.features.authentication.users.interfaces.rest.routers.auth_router import (
    router as auth_router,
)
from app.features.authentication.users.interfaces.rest.routers.users_router import (
    router as users_router,
)
from app.features.authentication.students.interfaces.rest.routers.students_router import (
    router as students_router,
)
from app.features.education.universities.interfaces.rest.routers.universities_router import (
    router as universities_router,
)
from app.features.authentication.users.infrastructure.middleware.auth_middleware import (
    AuthMiddleware,
)

from app.core.config.config import settings


def get_csv_path(filename: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "core", "data", filename)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_database_if_not_exists()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seeder
    async with async_session_maker() as session:
        repo = UniversityRepositoryImpl(session)

        count = await repo.count()

        if count == 0:
            print(">>> Seeding universities from CSV...")

            loader = UniversityCSVLoader()

            csv_path = get_csv_path("Malla-Curricular-Dataset-data.csv")
            print(">>> CSV PATH:", csv_path)

            universities = loader.load(csv_path)

            print(">>> COLUMNAS DEL CSV:", universities[0].keys())

            raw_names = {row["Universidad "].strip() for row in universities}

            use_case = CreateUniversityUseCase(repo)

            for raw in raw_names:
                name, acronym = UniversityCSVLoader.parse(raw)
                try:
                    await use_case.execute(name, acronym)
                except ValueError:
                    pass

            print(">>> Universities seeded successfully.")

    yield

app = FastAPI(
    title="EduGraph API",
    description="The RESTAPI application documentation for EduGraph",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
    lifespan=lifespan,
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
app.include_router(universities_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
