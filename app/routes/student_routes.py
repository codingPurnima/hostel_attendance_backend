from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user, require_resident
from app.models.attendance import Attendance

router = APIRouter(dependencies=[Depends(require_resident)])

@router.get("/profile")
def get_profile(current_user= Depends(get_current_user)):
    return {
        "name": current_user.name,
        "id": current_user.id,
        "room": current_user.room,
        "email": current_user.email,
        "status": current_user.status
    }


@router.get("/attendance")
def get_attendance(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    records = db.query(Attendance).filter(
        Attendance.student_id == current_user.id
    ).order_by(Attendance.date.desc()).all()

    return [
        {
            "date": r.date,
            "timestamp": r.timestamp
        }
        for r in records
    ]