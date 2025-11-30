from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import String

from app.features.shared.infrastructure.persistence.sql_alchemist.base.base import Base

class StudyPlanCycleModel(Base):
    __tablename__ = "study_plan_cycles"

    id = Column(String(36), primary_key=True, nullable=False)
    cycle_number = Column(Integer, nullable=False)

    study_plan_id = Column(String(36), ForeignKey("study_plans.id"), nullable=False)

    study_plan = relationship("StudyPlanModel", back_populates="cycles")
    courses = relationship("StudyPlanCourseModel", back_populates="cycle", cascade="all, delete-orphan")
