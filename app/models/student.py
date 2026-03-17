from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Enum
from app.database import Base
from app.models.enums import StudentStatusEnum

class Student(Base):
    __tablename__= "students"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(200), nullable= False)
    status = Column(Enum(StudentStatusEnum), default=StudentStatusEnum.active, nullable= False)
    penalty_count = Column(Integer, default=0)
