from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from datetime import datetime, date
import ast
import numpy as np

from app.database import get_db
from app.models.attendance import Attendance
from app.models.settings import Settings
from app.core.security import get_current_user
from app.services.face_service import generate_embedding
from app.models.enums import StudentStatusEnum

router = APIRouter(prefix="/attendance", tags=["Attendance"])

THRESHOLD = 0.6

@router.post("/mark")
async def mark_attendance(
    file: UploadFile = File(...),
    ssid: str = "",   # currently connected ssid coming from frontend later
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
        return {"error": "Attendance already marked"}

    # Check student status
    if current_user.status != StudentStatusEnum.active:
        return {"error": "Attendance not allowed"}

    # Get settings
    settings = db.query(Settings).first()

    if not settings:
        return {"error": "Settings not configured"}

    # Time check
    now = datetime.now().time()
    if not (settings.start_time <= now <= settings.end_time):
        return {"error": "Outside attendance time window"}

    # WiFi check
    if ssid != settings.wifi_ssid:
        return {"error": "Not connected to hostel WiFi"}

    # Face verification
    image_bytes = await file.read()
    new_embedding = generate_embedding(image_bytes)

    if new_embedding is None:
        return {"error": "Face not detected"}

    stored_embedding = ast.literal_eval(current_user.face_embedding)

    emb1 = np.array(new_embedding)
    emb2 = np.array(stored_embedding)

    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    if similarity < THRESHOLD:
        return {"error": "Face does not match"}

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