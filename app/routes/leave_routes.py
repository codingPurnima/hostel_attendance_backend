from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.leave_request import LeaveRequest
from app.models.return_request import ReturnRequest
from app.core.security import get_current_user

router= APIRouter()

@router.post("/leave-request")
def request_leave(
    start_date: date,
    end_date: date,
    current_user= Depends(get_current_user),
    db: Session= Depends(get_db)
):
    leave= LeaveRequest(
        student_id= current_user.id,
        start_date= start_date,
        end_date= end_date
    )

    db.add(leave)
    db.commit()

    return{"message": "Leave request submitted"}


@router.post("/early-return")
def early_return(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    request = ReturnRequest(
        student_id=current_user.id
    )

    db.add(request)
    db.commit()

    return {"message": "Return request submitted"}