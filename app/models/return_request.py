from sqlalchemy import Column, Integer, ForeignKey, Date, String
from app.database import Base
from app.models.enums import AttendanceStatusEnum
from datetime import date

class ReturnRequest(Base):
    __tablename__ = "return_requests"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    request_date= Column(Date, default=date.today)
    status = Column(String(50), default=AttendanceStatusEnum.pending)