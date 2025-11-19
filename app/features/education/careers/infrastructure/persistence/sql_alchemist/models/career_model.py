from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.features.shared.infrastructure.persistence.sql_alchemist.base.base import Base

class CareerModel(Base):
    __tablename__ = "careers"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(86), nullable=False)
    program = Column(String(16), nullable=False)
    university_id = Column(String(36), ForeignKey("universities.id"), nullable=False)

    university = relationship("UniversityModel", back_populates="careers")

    courses = relationship("CourseModel", back_populates="career", cascade="all, delete-orphan")
