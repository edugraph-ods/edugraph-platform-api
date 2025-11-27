from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.features.shared.infrastructure.persistence.sql_alchemist.base.base import Base

class StudyPlanModel(Base):
    __tablename__ = "study_plans"

    id = Column(String(36), primary_key=True, nullable=False)
    name = Column(String(36), nullable=False)
    max_credits = Column(Integer, nullable=False)

    student_id = Column(String(36), ForeignKey("students.id"), nullable=False)
    career_id = Column(String(36), ForeignKey("careers.id"), nullable=False)

    cycles = relationship("StudyPlanCycleModel", back_populates="study_plan", cascade="all, delete-orphan")
