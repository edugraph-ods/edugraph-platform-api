from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class UniversityModel(Base):
    __tablename__ = "universities"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    acronym = Column(String(3), nullable=False)

    students = relationship("StudentModel", back_populates="university")
    careers = relationship("CareerModel", back_populates="university")

