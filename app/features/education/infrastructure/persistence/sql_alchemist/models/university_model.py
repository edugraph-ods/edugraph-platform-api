from sqlalchemy import Column, String, DateTime
from datetime import datetime, timezone

from app.features.authentication.infrastructure.persistence.sql_alchemist.models.user_model import Base

class UniversityModel(Base):
    __tablename__ = "universities"

    id = Column(String(24), primary_key=True, index=True)
    name = Column(String(255), nullable=False)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

