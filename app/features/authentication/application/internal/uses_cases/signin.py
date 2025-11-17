from app.features.authentication.domain.repositories.auth_service import AuthService, UserRepository

"""
SignInUseCase is an abstract base class that defines the interface for sign-in use cases.

Returns:
    SignInUseCase: The SignInUseCase instance.
"""
class SignInUseCase:
    def __init__(self, user_repository: UserRepository, auth_service: AuthService):
        self.user_repository = user_repository
        self.auth_service = auth_service

    """
    execute is an abstract method that executes the use case.

    Args:
        email (str): The user's email.
        password (str): The user's password.

    Returns:
        dict: The user's data.
    """
    async def execute(self, email: str, password: str) -> dict:
        user = await self.user_repository.get_user_by_email(email)
        if not user or not user.is_active:
            raise ValueError("Invalid credentials")
        if not self.auth_service.verify_password(password, user.hashed_password):
            raise ValueError("Invalid credentials")
        access_token = self.auth_service.create_access_token(
            data={"sub": user.email, "user_id": str(user.id)}
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user_id": user.id,
            "email": user.email
        }