from app.features.authentication.users.application.internal.outbound_services.hashing_service.hashing_service import \
    HashingService
from app.features.authentication.users.domain.models.entities.user import User
from app.features.authentication.students.domain.repositories.student_repository import StudentRepository
from app.features.authentication.users.domain.repositories.user_repository import UserRepository
from app.features.education.universities.domain.repositories.university_repository import UniversityRepository

"""
SignUpUseCase is an abstract base class that defines the interface for sign-up use cases.

Returns:
    SignUpUseCase: The SignUpUseCase instance.
"""
class SignUpUseCase:
    def __init__(self, user_repository: UserRepository, student_repository: StudentRepository, university_repository: UniversityRepository, hash_service: HashingService):
        self.user_repository = user_repository
        self.student_repository = student_repository
        self.university_repository = university_repository
        self.hash_service = hash_service

    """
    execute is an abstract method that executes the use case.

    Args:
        email (str): The user email.
        password (str): The user password.
        username (str | None, optional): The user username. Defaults to None.

    Returns:
        dict: The user data.
    """
    async def execute(self, email: str, password: str, name: str) -> dict:
        if await self.user_repository.user_exists(email):
            raise ValueError("User already exists with this email")

        user = User.create(email=email)
        user.password = self.hash_service.get_password_hash(password)

        acronym = User.extrac_university_acronym_from_email(user.email)

        university = await self.university_repository.find_by_acronym(acronym)
        if university is None:
            raise ValueError(
                "University not found for email domain. Please use an institutional email or contact support."
            )

        created_user = await self.user_repository.create_user(user)

        user_id = str(created_user.id)

        student = await self.student_repository.create_student(
            user_id=user_id,
            name=name,
            university_id=university.id
        )

        return {"message": "Account created successfully"}