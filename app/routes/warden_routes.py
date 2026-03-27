from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.leave_request import LeaveRequest
from app.models.return_request import ReturnRequest
from app.models.student import Student
from app.models import enums

router= APIRouter()

@router.post("/approve-leave/{leave_id}")
def approve_leave(
    leave_id: int, 
    db: Session= Depends(get_db)
):
    leave= db.query(LeaveRequest).filter(LeaveRequest.id== leave_id).first()
    if not leave:
        return {"error": "Leave not found"}
    
    leave.status= enums.LeaveStatusEnum.approved

    student= db.query(Student).filter(Student.id== leave.student_id).first()
    student.status= enums.StudentStatusEnum.onleave

    db.commit()
    return {"message": "Leave approved"}


@router.post("/reject-leave/{leave_id}")
def reject_leave(leave_id: int, db: Session = Depends(get_db)):

    leave = db.query(LeaveRequest).filter(LeaveRequest.id == leave_id).first()

    if not leave:
        return {"error": "Leave not found"}

    leave.status = "REJECTED"

    db.commit()

    return {"message": "Leave rejected"}


@router.post("/approve-return/{request_id}")
def approve_return(request_id: int, db: Session = Depends(get_db)):

    req = db.query(ReturnRequest).filter(ReturnRequest.id == request_id).first()

    if not req:
        return {"error": "Request not found"}

    req.status = enums.EarlyReturnRequestEnum.approved

    student = db.query(Student).filter(Student.id == req.student_id).first()
    student.status = enums.StudentStatusEnum.active

    db.commit()

    return {"message": "Student reactivated"}