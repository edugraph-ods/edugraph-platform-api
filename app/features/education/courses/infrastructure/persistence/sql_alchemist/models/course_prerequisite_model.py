from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

from app.features.shared.infrastructure.persistence.sql_alchemist.base.base import Base


class CoursePrerequisiteModel(Base):
    __tablename__ = "course_prerequisites"

    id = Column(String(36), primary_key=True)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    prerequisite_id = Column(String(36), ForeignKey("courses.id"), nullable=False)

    course = relationship("CourseModel", foreign_keys=[course_id], back_populates="prerequisites")
    prerequisite = relationship("CourseModel", foreign_keys=[prerequisite_id])
