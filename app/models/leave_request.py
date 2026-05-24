from sqlalchemy import Column, Integer, ForeignKey, Date, String, DateTime, Enum
from datetime import datetime, UTC
from sqlalchemy.sql import func
from app.database import Base
from app.models.enums import AttendanceStatusEnum, LeaveStatusEnum

class LeaveRequest(Base):
    __tablename__ = "leave_requests"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    status = Column(Enum(LeaveStatusEnum), default=LeaveStatusEnum.pending)
    reason= Column(String, nullable=False)
    created_at= Column(DateTime(timezone=True), server_default=func.now())