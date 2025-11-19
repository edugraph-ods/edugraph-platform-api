from sqlalchemy import Column, String

from app.features.authentication.users.infrastructure.persistence.sql_alchemist.models.user_model import Base

class UniversityModel(Base):
    __tablename__ = "universities"

    id = Column(String(24), primary_key=True, index=True)
    name = Column(String(255), nullable=False)

