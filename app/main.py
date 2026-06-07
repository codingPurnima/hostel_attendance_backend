from fastapi import FastAPI
from app.routes import auth_routes,face_routes, test_routes, attendance_routes, leave_routes, warden_routes, student_routes
from app.database import Base, engine, SessionLocal
from app.models import user
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import logging

from app.services.leave_service import reactivate_expired_leaves

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix= "/auth", tags=["Authentication"])
app.include_router(test_routes.router, tags=["Test"])
app.include_router(face_routes.router, prefix="/face", tags=["Face"])
app.include_router(attendance_routes.router,prefix="/attendance",  tags=["Attendance"])
app.include_router(leave_routes.router, prefix="/leave", tags=["Leave"])
app.include_router(warden_routes.router, prefix='/warden', tags=['Warden Routes'])
app.include_router(student_routes.router, prefix="/student", tags=["Student Routes"])

Base.metadata.create_all(bind=engine) 
# creates table only if it does not exist, does not modify existing table, like it won't change columns or add or remove them

@app.get("/")
def home():
    return {"message": "Hostel Attendance API running"}


async def _reactivation_loop() -> None:
    """Background loop that reactivates students whose leave has ended.

    Runs immediately on startup and then once every 24 hours.
    """
    while True:
        db = SessionLocal()
        try:
            try:
                count = reactivate_expired_leaves(db)
                if count:
                    logger.info("Reactivation run completed: %d students reactivated", count)
                else:
                    logger.debug("Reactivation run completed: no students reactivated")
            except Exception:
                logger.exception("Error during reactivation run")
        finally:
            db.close()

        await asyncio.sleep(24 * 3600)


@app.on_event("startup")
async def _start_background_tasks():
    logger.info("Starting reactivation background task")
    asyncio.create_task(_reactivation_loop())