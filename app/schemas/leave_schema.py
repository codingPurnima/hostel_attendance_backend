from datetime import date

from pydantic import BaseModel, ConfigDict

class CreateLeave(BaseModel):
    start_date: date
    end_date: date
    reason: str

    model_config= ConfigDict(from_attributes= True)

class LeaveResponse(BaseModel):
    id: int
    start_date: date
    end_date: date
    reason: str
    status: str
    
    model_config= ConfigDict(from_attributes= True)

class CancelLeaveRequest(BaseModel):
    id: int

    model_config= ConfigDict(from_attributes=True)
