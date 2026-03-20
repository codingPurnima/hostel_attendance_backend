from sqlalchemy import Column, Integer, ForeignKey, Date, DateTime
from datetime import datetime
from app.database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    date = Column(Date)
    timestamp = Column(DateTime, default=datetime.utcnow)