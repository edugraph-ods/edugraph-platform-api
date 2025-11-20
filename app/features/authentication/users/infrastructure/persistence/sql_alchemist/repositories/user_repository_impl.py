from sqlalchemy import select, update
from app.features.authentication.users.domain.models.entities.user import User
from app.features.authentication.users.domain.repositories.user_repository import UserRepository
from app.features.authentication.users.infrastructure.persistence.sql_alchemist.models.user_model import UserModel
from datetime import datetime
from datetime import timezone

"""
UserRepositorySQL is a class that implements the UserRepository interface.
It provides methods for interacting with a database to perform user-related operations.

Attributes:
    db: The database session used to execute queries.
"""
class UserRepositoryImpl(UserRepository):
    def __init__(self, db_session):
        self.db = db_session

    """
    Gets a user by their email.
    
    Args:
        email (str): The user's email.
    
    Returns:
        User | None: The user found or None if not found.
    """
    def _to_domain(self, user_model: UserModel | None) -> User | None:
        if user_model is None:
            return None
        return User(
            email=user_model.email,
            id=user_model.id,
            password=user_model.password,
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
            recovery_code=user_model.recovery_code,
            recovery_code_expiration=user_model.recovery_code_expiration,
        )

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(UserModel).where(UserModel.email == email)
        )
        return self._to_domain(result.scalar_one_or_none())

    """
    Creates a new user.
    
    Args:
        user (User): The user to create.
    
    Returns:
        User: The created user.
    """
    async def create_user(self, user: User) -> User:
        user_model = UserModel(
            id=user.id,
            email=user.email,
            password=user.password,
            recovery_code=user.recovery_code,
            recovery_code_expiration=user.recovery_code_expiration,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

        self.db.add(user_model)
        await self.db.commit()
        await self.db.refresh(user_model)
        
        user.id = user_model.id
        user.created_at = user_model.created_at
        user.updated_at = user_model.updated_at
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

    async def get_user_by_id(self, user_id: str) -> User | None:
        result = await self.db.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        return self._to_domain(result.scalar_one_or_none())

    async def update_password(self, user_id: str, hashed_password: str) -> None:
        await self.db.execute(
            update(UserModel)
            .where(UserModel.id == user_id)
            .values(
                password=hashed_password,
                updated_at=datetime.now(timezone.utc),
            )
        )
        await self.db.commit()