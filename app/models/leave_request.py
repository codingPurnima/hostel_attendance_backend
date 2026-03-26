from sqlalchemy import Column, Integer, ForeignKey, Date, String
from app.database import Base
from app.models.enums import AttendanceStatusEnum

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(String(50), default=AttendanceStatusEnum.pending)