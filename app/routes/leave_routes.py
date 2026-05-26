from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from app.database import get_db
from app.models.leave_request import LeaveRequest
from app.models.return_request import ReturnRequest
from app.core.security import get_current_user, require_resident
from app.models import enums
from app.schemas.leave_schema import LeaveResponse, CreateLeave, CancelLeaveRequest

router= APIRouter(dependencies=[Depends(require_resident)])

@router.post("/leave-request", response_model=LeaveResponse)
def request_leave(
    payload: CreateLeave,
    current_user= Depends(get_current_user),
    db: Session= Depends(get_db)
):
    existing= db.query(LeaveRequest).filter(
        LeaveRequest.student_id== current_user.id,
        LeaveRequest.status== enums.LeaveStatusEnum.pending
    ).first()
    
    if existing:
        raise HTTPException(status_code=409, detail= "Can't create new leave while one is pending")
    
    leave= LeaveRequest(
        student_id= current_user.id,
        start_date= payload.start_date,
        end_date= payload.end_date,
        reason= payload.reason
    )

    db.add(leave)
    db.commit()
    db.refresh(leave)

    return leave

@router.get("/my-leaves", response_model=list[LeaveResponse])
def get_my_leaves(
    current_user= Depends(get_current_user),
    db: Session= Depends(get_db)
):
    leaves= db.query(LeaveRequest).filter(
        LeaveRequest.student_id== current_user.id
    ).order_by(LeaveRequest.created_at.desc()).all()

    return leaves

@router.delete("/cancel-leave/{leave_id}")
def cancel_leave(
    leave_id: int,
    db: Session= Depends(get_db),
    current_user= Depends(get_current_user)
):
    leave= db.query(LeaveRequest).filter(
        LeaveRequest.id== leave_id,
        LeaveRequest.student_id== current_user.id
    ).first()

    if not leave:
        raise HTTPException(status_code=404, detail= "Leave not found")
    
    if leave.status!= enums.LeaveStatusEnum.pending:
        raise HTTPException(status_code=400, detail= "Only pending requests can be cancelled")
    
    leave.status= enums.LeaveStatusEnum.cancelled

    db.commit()

    return {"message": "Leave cancelled successfully"}

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

    return {"message": "Return request submitted. Pending."}