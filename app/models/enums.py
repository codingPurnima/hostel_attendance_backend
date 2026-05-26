from enum import Enum

class RoleEnum(str, Enum):
    warden= "warden"
    student= "student"

class StudentStatusEnum(str, Enum):
    active="active"
    onleave= "onLeave"

class AttendanceStatusEnum(str, Enum):
    pending= "pending"
    marked= "marked"
    absent= "absent"

class LeaveStatusEnum(str, Enum):
    approved= "approved"
    rejected= "rejected"
    pending= "pending"
    cancelled= "cancelled"
    
class EarlyReturnRequestEnum(str, Enum):
    approved= "approved"
    rejected= "rejected"
    pending= "pending"