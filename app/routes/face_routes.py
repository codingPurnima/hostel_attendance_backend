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

# temporary endpoint for testing
@router.get("/test-import")
def test_import():
    try:
        from deepface import DeepFace
        return {"message": "DeepFace imported successfully"}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "error": type(e).__name__,
            "detail": str(e)
        }

@router.get("/test-model")
def test_model():
    from deepface import DeepFace
    import numpy as np

    img = np.zeros((160, 160, 3), dtype=np.uint8)

    try:
        DeepFace.build_model("Facenet")
        return {"status": "model loaded"}

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {
            "error": type(e).__name__,
            "detail": str(e)
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