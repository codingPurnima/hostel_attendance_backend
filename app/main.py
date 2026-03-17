from fastapi import FastAPI
from app.routes import auth_routes
from app.database import Base, engine
from app.models import student

app= FastAPI()
app.include_router(auth_routes.router, tags=["Authentication"])

Base.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {"message": "Hostel Attendance API running"}