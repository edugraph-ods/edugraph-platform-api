from sqlalchemy import select
from app.features.authentication.domain.models.user import User
from app.features.authentication.domain.repositories.auth_service import UserRepository
from app.features.authentication.infrastructure.persistence.models.models import UserModel

"""
UserRepositorySQL is a class that implements the UserRepository interface.
It provides methods for interacting with a database to perform user-related operations.

Attributes:
    db: The database session used to execute queries.
"""
class UserRepositorySQL(UserRepository):
    def __init__(self, db_session):
        self.db = db_session

    """
    Gets a user by their email.
    
    Args:
        email (str): The user's email.
    
    Returns:
        User | None: The user found or None if not found.
    """
    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user_model = result.scalar_one_or_none()
        if user_model:
            return User(
                id=user_model.id,
                email=user_model.email,
                hashed_password=user_model.hashed_password,
                full_name=user_model.full_name,
                is_active=user_model.is_active,
                created_at=user_model.created_at,
                updated_at=user_model.updated_at
            )
        return None

    """
    Creates a new user.
    
    Args:
        user (User): The user to create.
    
    Returns:
        User: The created user.
    """
    async def create_user(self, user: User) -> User:
        user_model = UserModel(
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
        self.db.add(user_model)
        await self.db.commit()
        await self.db.refresh(user_model)
        
        user.id = user_model.id
        return user

    """
    Checks if a user with the provided email exists.
    
    Args:
        email (str): The user's email.
    
    Returns:
        bool: True if the user exists, False otherwise.
    """
    async def user_exists(self, email: str) -> bool:
        result = await self.db.execute(
            select(UserModel.id).where(UserModel.email == email)
        )
        return result.scalar_one_or_none() is not None