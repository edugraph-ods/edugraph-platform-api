from app.features.authentication.users.application.internal.outbound_services.hashing_service.hashing_service import \
    HashingService
from app.features.authentication.users.domain.models.user import User
from app.features.authentication.students.domain.repositories.student_repository import StudentRepository
from app.features.authentication.users.domain.repositories.user_repository import UserRepository

"""
SignUpUseCase is an abstract base class that defines the interface for sign-up use cases.

Returns:
    SignUpUseCase: The SignUpUseCase instance.
"""
class SignUpUseCase:
    def __init__(self, user_repository: UserRepository, student_repository: StudentRepository, hash_service: HashingService):
        self.user_repository = user_repository
        self.student_repository = student_repository
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

        created_user = await self.user_repository.create_user(user)

        user_id = str(created_user.id)

        student = await self.student_repository.create_student(
            user_id=user_id,
            name=name
        )

        return {"message": "Account created successfully"}