from datetime import date
from sqlalchemy.orm import Session
import logging

from app.models.leave_request import LeaveRequest
from app.models.user import User
from app.models import enums

logger = logging.getLogger(__name__)


def reactivate_expired_leaves(db: Session) -> int:
    """Activate students whose approved leave has ended.

    Returns the number of students reactivated.
    """
    today = date.today()

    expired_leaves = (
        db.query(LeaveRequest)
        .filter(
            LeaveRequest.status == enums.LeaveStatusEnum.approved,
            LeaveRequest.end_date < today,
        )
        .all()
    )

    reactivated = 0
    for leave in expired_leaves:
        student = db.query(User).filter(User.id == leave.student_id).first()
        if student and student.status == enums.StudentStatusEnum.onleave:
            logger.info("Reactivating student id=%s for leave id=%s", student.id, leave.id)
            student.status = enums.StudentStatusEnum.active
            reactivated += 1

    if reactivated:
        db.commit()
        logger.info("Reactivated %d students whose leave expired before %s", reactivated, today)

    return reactivated
