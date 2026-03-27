from enum import Enum

# class RoleEnum(str, Enum):
#     warden= "warden"
#     resident= "resident"

class StudentStatusEnum(str, Enum):
    active="active"
    onleave= "onLeave"

class AttendanceStatusEnum(str, Enum):
    pending= "pending"
    marked= "marked"

class LeaveStatusEnum(str, Enum):
    approved= "approved"
    rejected= "rejected"
    pending= "pending"
    
class EarlyReturnRequestEnum(str, Enum):
    approved= "approved"
    rejected= "rejected"
    pending= "pending"