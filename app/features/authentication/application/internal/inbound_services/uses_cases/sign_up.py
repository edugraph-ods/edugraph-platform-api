from app.features.authentication.application.internal.outbound_services.hashing_service.hashing_service import \
    HashingService
from app.features.authentication.domain.models.user import User
from app.features.authentication.domain.repositories.auth_repository import UserRepository

"""
SignUpUseCase is an abstract base class that defines the interface for sign-up use cases.

Returns:
    SignUpUseCase: The SignUpUseCase instance.
"""
class SignUpUseCase:
    def __init__(self, user_repository: UserRepository, hash_service: HashingService):
        self.user_repository = user_repository
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
    async def execute(self, email: str, password: str, username: str | None = None) -> dict:
        if await self.user_repository.user_exists(email):
            raise ValueError("User already exists with this email")

        user = User.create(email=email, username=username)
        user.password = self.hash_service.get_password_hash(password)

        await self.user_repository.create_user(user)

        return {"message": "Account created successfully"}