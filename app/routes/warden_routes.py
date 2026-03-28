from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.leave_request import LeaveRequest
from app.models.return_request import ReturnRequest
from app.models.student import Student
from app.models import enums
from app.models.attendance import Attendance

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

@router.get("/students")
def get_students(
    db: Session= Depends(get_db)
):
    students= db.query(Student).all()

    return[
        {
            "id": s.id,
            "room": s.room,
            "email": s.email,
            "status": s.status
        }
        for s in students
    ]

@router.get("/attendance/today")
def today_attendance(db: Session = Depends(get_db)):
    today = date.today()

    students= db.query(Student).all()
    records = db.query(Attendance).filter(Attendance.date == today).all()

    present_ids= {a.student_id for a in records}

    result=[]
    
    for s in students:
        result.append({
            "student_id": s.id,
            "room": s.room,
            "status": enums.AttendanceStatusEnum.marked if s.id in present_ids else enums.AttendanceStatusEnum.absent
        })
    return result


@router.get("/attendance/all")
def all_attendance(db: Session = Depends(get_db)):
    records = db.query(Attendance).all()

    return [
        {
            "student_id": r.student_id,
            "date": r.date,
            "timestamp": r.timestamp
        }
        for r in records
    ]

@router.get("/leave-requests")
def get_leave_requests(db: Session = Depends(get_db)):
    requests = db.query(LeaveRequest).all()

    return [
        {
            "id": r.id,
            "student_id": r.student_id,
            "start_date": r.start_date,
            "end_date": r.end_date,
            "status": r.status
        }
        for r in requests
    ]


@router.get("/return-requests")
def get_return_requests(db: Session = Depends(get_db)):
    requests = db.query(ReturnRequest).all()

    return [
        {
            "id": r.id,
            "student_id": r.student_id,
            "date": r.request_date,
            "status": r.status
        }
        for r in requests
    ]