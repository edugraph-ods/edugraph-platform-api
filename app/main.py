import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from contextlib import asynccontextmanager

from app.features.authentication.users.infrastructure.persistence.sql_alchemist.models.user_model import Base
import app.features.authentication.students.infrastructure.persistence.sql_alchemist.models.student_model
import app.features.education.universities.infrastructure.persistence.sql_alchemist.models.university_model
from app.features.education.careers.infrastructure.persistence.sql_alchemist.repositories.career_repository_impl import \
    CareerRepositoryImpl
from app.features.education.courses.infrastructure.persistence.sql_alchemist.repositories.course_prerequisite_repository_impl import \
    CoursePrerequisiteRepositoryImpl
from app.features.education.courses.infrastructure.persistence.sql_alchemist.repositories.course_repository_impl import \
    CourseRepositoryImpl

from app.features.education.universities.infrastructure.persistence.sql_alchemist.repositories.university_repository_impl import (
    UniversityRepositoryImpl,
)

from app.features.shared.infrastructure.persistence.sql_alchemist.start.session import (
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
from app.features.education.careers.interfaces.rest.routers.universities_careers_router import (
    router as universities_careers_router,
)
from app.features.education.careers.interfaces.rest.routers.careers_router import (
    router as careers_router,
)
from app.features.education.courses.interfaces.rest.routers.carrers_courses_router import (
    router as careers_courses_router,
)
from app.features.education.courses.interfaces.rest.routers.course_router import (
    router as course_router,
)
from app.features.education.academic_progress.interfaces.rest.routers.academic_progress_router import (
    router as academic_progress_router,
)
from app.features.education.academic_progress.interfaces.rest.routers.min_prerequisite_course_router import (
    router as min_prerequisite_course_router,
)
from app.features.authentication.users.infrastructure.middleware.auth_middleware import (
    AuthMiddleware,
)

from app.core.config.config import settings
from app.features.shared.infrastructure.seed.csv.course_prerrequisite_seeder import CoursePrerequisiteSeeder
from app.features.shared.infrastructure.seed.csv.seed_careers import CareerSeeder
from app.features.shared.infrastructure.seed.csv.seed_courses import CourseSeeder
from app.features.shared.infrastructure.seed.csv.seed_universities import UniversitySeeder


def get_csv_path(filename: str) -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "core", "data", filename)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await create_database_if_not_exists()
    except Exception:
        pass

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seeder
    async with async_session_maker() as session:
        university_repo = UniversityRepositoryImpl(session)
        career_repo = CareerRepositoryImpl(session)
        course_repo = CourseRepositoryImpl(session)
        course_prereq_repo = CoursePrerequisiteRepositoryImpl(session)

        uni_count = await university_repo.count()
        if uni_count == 0:
            csv_path = get_csv_path("Malla-Curricular-Dataset-data.csv")

            # Seed universities
            uni_seeder = UniversitySeeder(session, university_repo)
            await uni_seeder.seed(csv_path)
            print(">>> Universities seeded successfully.")

            # Seed careers
            career_seeder = CareerSeeder(session, career_repo, university_repo)
            await career_seeder.seed(csv_path)
            print(">>> Careers seeded successfully.")

            # Seed courses
            course_seeder = CourseSeeder(session, course_repo, career_repo)
            await course_seeder.seed(csv_path)
            print(">>> Courses seeded successfully.")

            # Seed course prerequisite
            course_prereq_seeder = CoursePrerequisiteSeeder(session, course_repo, course_prereq_repo)
            await course_prereq_seeder.seed(csv_path)
            print(">>> Course prerequisites seeded successfully.")

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
        "/api/v1/universities",
    },
    public_prefixes=(),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.backend_cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["Authorization", "Content-Type"],
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
app.include_router(universities_careers_router)
app.include_router(careers_router)
app.include_router(careers_courses_router)
app.include_router(course_router)
app.include_router(academic_progress_router)
app.include_router(min_prerequisite_course_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
    )
