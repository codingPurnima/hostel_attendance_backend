from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from typing import List
from app.core.security import get_current_user
from app.services.face_service import generate_embedding
from app.database import SessionLocal, get_db
import numpy as np
import ast

router= APIRouter()

@router.post("/register")
async def register_face(
    file: UploadFile= File(...),
    dummy: str= Form(None),
    current_user= Depends(get_current_user),
    db= Depends(get_db)
):
    image_bytes= await file.read()
    embedding= generate_embedding(image_bytes)
    
    current_user.face_embedding= str(embedding)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return{"message": "Face registered successfully"}
# , description="Upload multiple images", media_type="multipart/form-data"

# VERIFY USER IMAGE DURING ATTENDANCE
@router.post("/verify")
async def verify_face(
    file: UploadFile= File(...),
    current_user= Depends(get_current_user)
):
# GENERATE EMBEDDING FOR CAPTURED IMAGE 
    image_bytes= await file.read()
    new_embedding= generate_embedding(image_bytes)
    if new_embedding is None:
        raise HTTPException(
            status_code=400, detail="Face not detected"
        )
    
# ACCESS FROM DATABASE 
    if not current_user.face_embedding:
        raise HTTPException(
            status_code=400, detail="Face not registered"
        )
    
    stored_embedding= ast.literal_eval(current_user.face_embedding)

    emb1= np.array(new_embedding)
    emb2= np.array(stored_embedding)

# COSINE SIMILARITY
    similarity= np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))

    THRESHOLD= 0.75
    is_match= bool(similarity> THRESHOLD)

    return{
        "match": bool(is_match),
        "similarity": float(similarity)
    }

# PART OF REGISTER ENDPOINT- INPUT MULTIPLE FILES WASN'T WORKING WITH SWAGGER, SO SKIPPED FOR THE TIME BEING, ADD LATER
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