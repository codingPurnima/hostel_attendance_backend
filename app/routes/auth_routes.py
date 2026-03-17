from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.student import Student
from app.schemas.auth_schema import RegisterSchema, LoginSchema
from app.core.security import decode_refresh_token, hash_password, verify_password, create_access_token, create_refresh_token
from app.database import get_db

router= APIRouter()

# REGISTER RESIDENT
@router.post("/register", status_code=201)
def register_student(user: RegisterSchema, db: Session= Depends(get_db)):
    existing= db.query(Student).filter(Student.email== user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail='User exists already')
    
    new_user= Student(
    #   table attributes= parameters being passed by user in the format of Register schema
        name= user.name,
        room= user.room,
        email= user.email,
        hashed_password= hash_password(user.password)
    )
    db.add(new_user)
    db.commit()

    return {"message": "Resident registered successfully"}

# RESIDENT LOGIN
@router.post("/login")
def login(user: LoginSchema, db: Session= Depends(get_db)):
    db_user = db.query(Student).filter(Student.email == user.email).first()

    if not db_user:
        return {"error": "Invalid email"}

# order of parameters matters
    if not verify_password(user.password, db_user.hashed_password ): 
        return {"error": "Invalid password"}

    access_token = create_access_token({"sub": db_user.email, "user_id": db_user.id})
    refresh_token= create_refresh_token({"sub": db_user.email, "user_id": db_user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(refresh_token: str):
    payload= decode_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    new_access_token= create_access_token({
        "sub": payload["sub"],
        "user_id": payload["user_id"]
    })

    return{
        "access_token": new_access_token,
        "token_type": "bearer"
    }
