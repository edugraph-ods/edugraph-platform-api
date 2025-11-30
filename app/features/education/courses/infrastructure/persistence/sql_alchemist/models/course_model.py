from sqlalchemy import Column, String, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.features.shared.infrastructure.persistence.sql_alchemist.base.base import Base


class CourseModel(Base):
    __tablename__ = "courses"
    __table_args__ = (
        UniqueConstraint("career_id", "code", name="uq_courses_career_code"),
    )

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    code = Column(String(16), nullable=False)
    cycle = Column(Integer, nullable=False)
    credits = Column(Integer, nullable=False)

    career_id = Column(String(36), ForeignKey("careers.id"), nullable=False)

    career = relationship("CareerModel", back_populates="courses")
    prerequisites = relationship(
        "CoursePrerequisiteModel",
        back_populates="course",
        cascade="all, delete-orphan",
        foreign_keys="CoursePrerequisiteModel.course_id"
    )