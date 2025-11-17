from app.features.authentication.application.internal.outbound_services.hashing_service.hashing_service import \
    HashingService
from app.features.authentication.application.internal.outbound_services.token_service.token_service import TokenService
from app.features.authentication.domain.models.user import User
from app.features.authentication.domain.repositories.auth_repository import AuthService, UserRepository

"""
SignUpUseCase is an abstract base class that defines the interface for sign-up use cases.

Returns:
    SignUpUseCase: The SignUpUseCase instance.
"""
class SignUpUseCase:
    def __init__(self, user_repository: UserRepository, hash_service: HashingService, token_service: TokenService):
        self.user_repository = user_repository
        self.hash_service = hash_service
        self.token_service = token_service
    """
    execute is an abstract method that executes the use case.

    Args:
        email (str): The user's email.
        password (str): The user's password.
        full_name (str, optional): The user's full name. Defaults to None.

    Returns:
        dict: The user's data.
    """
    async def execute(self, email: str, password: str, full_name: str = None) -> dict:
        if await self.user_repository.user_exists(email):
            raise ValueError("User already exists with this email")

        user = User.create(email=email, full_name=full_name)
        user.hashed_password = self.hash_service.get_password_hash(password)

        created_user = await self.user_repository.create_user(user)

        access_token = self.token_service.create_access_token(
            data={"sub": created_user.email, "user_id": str(created_user.id)}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": created_user.id,
            "email": created_user.email
        }