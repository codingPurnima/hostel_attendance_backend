# Smart Hostel Attendance System - Backend

A secure hostel attendance and leave management backend built using FastAPI, MySQL, JWT Authentication, and OpenCV-based facial verification.

---

## Technology Stack

| Category | Technologies |
|-----------|-------------|
| Backend | FastAPI, Python |
| Database | MySQL, SQLAlchemy |
| Authentication | JWT, Passlib |
| Face Recognition | OpenCV, InsightFace, NumPy |

---

## Features

### Authentication

- User Registration
- User Login
- JWT Access Tokens
- JWT Refresh Tokens
- Protected Routes

### Face Recognition

- Face Registration
- Face Verification using Facial Embeddings
- Cosine Similarity Matching
- Configurable Verification Threshold

### Attendance Management

- Facial Verification Based Attendance
- Attendance Window Enforcement
- Hostel WiFi Restriction
- Prevention of Duplicate Attendance
- Attendance History

### Leave Management

- Leave Request Submission
- Leave Approval Workflow
- Leave Rejection Workflow
- Leave Cancellation
- Resident Status Updates

---

## Project Structure

```text
app/
├── core/
│   └── security.py
│   └── config.py
├── database.py
├── models/
│   ├── user.py
│   ├── attendance.py
│   ├── enums.py
│   ├── leave_request.py
│   ├── return_request.py
│   └── settings.py
├── routes/
│   ├── auth_routes.py
│   ├── face_routes.py
│   ├── attendance_routes.py
│   ├── leave_routes.py
│   ├── student_routes.py
│   └── warden_routes.py
├── schemas/
│   └── auth_schema.py
│   └── leave_schema.py
├── services/
│   └── face_service.py
│   └── leave_service.py
└── main.py
```

---

## Attendance Workflow

1. Resident logs in.
2. Resident registers facial data.
3. During attendance window:
   - Capture face image
   - Verify hostel WiFi
   - Verify timing
   - Verify identity
4. Attendance recorded.

---

## API Modules

### Authentication

```text
/auth/register
/auth/login
/auth/refresh
```

### Face Recognition

```text
/face/register
/face/verify
```

### Attendance

```text
/attendance/mark
```

### Leave Management

```text
/leave/leave-request
/leave/my-leaves
/leave/cancel-leave/{leave_id}
/leave/early-return
```

### Wardens

```text
/warden/students
/warden/attendance/today
/warden/leave-requests
/warden/return-requests
/warden/approve-leave/{leave_id}
/warden/reject-leave/{leave_id}
/warden/approve-return/{request_id}
```
### Students

```text
/student/profile
/student/attendance
```

---

## Future Enhancements

- QR-Based Leave Pass
- Entry/Exit Tracking
- Complaint Management
- Mess Fee Management
- Push Notifications
- Multi-Hostel Support

---

## Related Repository

Frontend Repository:

https://github.com/codingPurnima/hostel_attendance_frontend

---

## Author

Built as a full-stack hostel operations management platform focusing on attendance automation and resident workflow management.
### Deployment note: 
The face recognition module works correctly in local testing. The free Render instance does not provide enough memory to initialize the face recognition model, resulting in the service being terminated during model loading. Deploying on an instance with higher memory or a dedicated inference service resolves this limitation.
