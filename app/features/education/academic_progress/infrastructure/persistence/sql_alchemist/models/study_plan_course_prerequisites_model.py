from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.features.shared.infrastructure.persistence.sql_alchemist.base.base import Base

class StudyPlanCoursePrerequisiteModel(Base):
    __tablename__ = "study_plan_course_prerequisites"

    id = Column(String(36), primary_key=True, nullable=False)

    study_plan_course_id = Column(String(36), ForeignKey("study_plan_courses.id"), nullable=False)
    prerequisite_course_code = Column(String(36), nullable=False)

    course = relationship("StudyPlanCourseModel", back_populates="prerequisites")
