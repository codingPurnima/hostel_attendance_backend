from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from datetime import datetime, date
import ast
import numpy as np

from app.database import get_db
from app.models.attendance import Attendance
from app.models.settings import Settings
from app.core.security import get_current_user, require_resident
from app.services.face_service import generate_embedding
from app.models.enums import StudentStatusEnum

router = APIRouter(tags=["Attendance"], dependencies=[Depends(require_resident)])

THRESHOLD = 0.75

@router.post("/mark")
async def mark_attendance(
    file: UploadFile = File(...),
    ssid: str = Form(...),   # currently connected ssid coming from frontend later
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):    
    # Check if already marked today
    today = date.today()

    existing = db.query(Attendance).filter(
        Attendance.student_id == current_user.id,
        Attendance.date == today
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Attendance already marked"
        )

    # Check student status
    if current_user.status != StudentStatusEnum.active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Attendance not allowed"
        )

    # Get settings
    settings = db.query(Settings).first()

    if not settings:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Settings not configured"
        )

    # Time check
    now = datetime.now().time()
    if not (settings.start_time <= now <= settings.end_time):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Outside attendance time window"
        )

    # WiFi check
    # temporarily include AndroidWifi
    allowed_ssids=[settings.wifi_ssid, "AndroidWifi"]
    if ssid not in allowed_ssids:
        print("FRONTEND SSID:", repr(ssid))
        print("DB SSID:", repr(settings.wifi_ssid))
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not connected to hostel WiFi"
        )

    # Face verification
    image_bytes = await file.read()
    new_embedding = generate_embedding(image_bytes)

    if new_embedding is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Face not detected"
        )

    stored_embedding = ast.literal_eval(current_user.face_embedding)

    emb1 = np.array(new_embedding)
    emb2 = np.array(stored_embedding)

    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    if similarity < THRESHOLD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Face does not match"
        )

    # Mark attendance
    new_attendance = Attendance(
        student_id=current_user.id,
        date=today
    )

    db.add(new_attendance)
    db.commit()

    return {
        "message": "Attendance marked",
        "similarity": float(similarity)
    }