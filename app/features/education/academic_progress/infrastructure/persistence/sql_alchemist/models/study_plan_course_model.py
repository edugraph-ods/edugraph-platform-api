from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.features.shared.infrastructure.persistence.sql_alchemist.base.base import Base

class StudyPlanCourseModel(Base):
    __tablename__ = "study_plan_courses"

    id = Column(String(36), primary_key=True, nullable=False)

    cycle_id = Column(String(36), ForeignKey("study_plan_cycles.id"), nullable=False)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)

    status = Column(String(36), default="NOT_STARTED")
    name = Column(String(56), nullable=False)
    credits = Column(Integer, nullable=False)

    cycle = relationship("StudyPlanCycleModel", back_populates="courses")
    prerequisites = relationship("StudyPlanCoursePrerequisiteModel", back_populates="course", cascade="all, delete-orphan")
