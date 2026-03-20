from sqlalchemy import Column, Integer, Time, String
from app.database import Base

class Settings(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(Time)
    end_time = Column(Time)
    wifi_ssid = Column(String(100))