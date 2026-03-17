from fastapi import FastAPI
from app.routes import test_routes

app= FastAPI()
app.include_router(test_routes.router, tags=["Test"])

@app.get("/")
def home():
    return {"message": "Hostel Attendance API running"}