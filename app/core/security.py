from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from app.core.config import settings
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.models.user import User
from app.models.enums import RoleEnum

SECRET_KEY= settings.SECRET_KEY
ALGORITHM= settings.ALGORITHM
security= HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str)-> str:
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password: str)-> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):  
    to_encode=data.copy()  
    expire= datetime.utcnow()+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) 
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict):
    to_encode= data.copy()
    expire= datetime.utcnow()+timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})

    return jwt.encode(
        to_encode, SECRET_KEY, algorithm=settings.ALGORITHM
    )

def decode_refresh_token(token: str):
    try:
        payload= jwt.decode(token, SECRET_KEY, algorithms=[settings.ALGORITHM])

        if payload.get("type")!= "refresh":
            raise Exception("Invalid token type")
        
        if payload is None:
            return None
        
        return payload
    except JWTError:
        return None
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    print("TOKEN RECEIVED:", token)

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        print("PAYLOAD:", payload)

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError as e:
        print("JWT ERROR:", str(e))

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user

def require_warden(current_user= Depends(get_current_user)):
    if current_user.role != RoleEnum.warden:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only wardens can access this"
        )
    return current_user

def require_resident(current_user= Depends(get_current_user)):
    if current_user.role!= RoleEnum.student:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only residents can access this"
        )
    return current_user