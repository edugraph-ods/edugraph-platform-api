from sqlalchemy import Column, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()
class CareerModel(Base):
    __tablename__ = "careers"

    id = Column(String(36), primary_key=True, index=True)
    name = Column(String(86), nullable=False)
    university_id = Column(String(36), nullable=False)

    university = relationship("UniversityModel", back_populates="careers")
