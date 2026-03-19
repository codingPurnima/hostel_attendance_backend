from fastapi import APIRouter, UploadFile, File, Depends, Form
from typing import List
from app.core.security import get_current_user
from app.services.face_service import generate_embedding
from app.database import SessionLocal, get_db

router= APIRouter()

@router.post("/register")
async def register_face(
    file: UploadFile= File(...),
    dummy: str= Form(None),
    current_user= Depends(get_current_user),
    db= Depends(get_db)
):
    # embeddings= []

    # for file in files:
    #     image_bytes= await file.read()
    #     embedding= generate_embedding(image_bytes)
    #     if embedding is not None:
    #         embeddings.append(embedding)

    # if len(embeddings)== 0:
    #     return {"error":"No valid face detected"}
    
    # avg_embedding= [sum(x)/len(x) for x in zip(*embeddings)]

    # current_user.face_embedding= str(avg_embedding)

    # db.add(current_user)
    # db.commit()


    image_bytes= await file.read()
    embedding= generate_embedding(image_bytes)
    if embedding is None:
        return {"error": "No valid face detected"}
    current_user.face_embedding= str(embedding)

    db.add(current_user)
    db.commit()
    
    return{"message": "Face registered successfully"}






# , description="Upload multiple images", media_type="multipart/form-data"