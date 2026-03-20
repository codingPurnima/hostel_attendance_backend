from fastapi import FastAPI
from app.routes import auth_routes,face_routes, test_routes, attendance_routes
from app.database import Base, engine
from app.models import student

app= FastAPI()
app.include_router(auth_routes.router, prefix= "/auth", tags=["Authentication"])
app.include_router(test_routes.router, tags=["Test"])
app.include_router(face_routes.router, prefix="/face", tags=["Face"])
app.include_router(attendance_routes.router, tags=["Attendance"])


Base.metadata.create_all(bind=engine) 
# creates table only if it does not exist, does not modify existing table, like it won't change columns or add or remove them

@app.get("/")
def home():
    return {"message": "Hostel Attendance API running"}