from fastapi import HTTPException
import numpy as np
import cv2
import logging
from typing import List

logger= logging.getLogger(__name__)

_DeepFace= None

# def get_deepface():
#     """
#     Lazily import DeepFace.
#     This prevents TensorFlow from loading during FastAPI startup.
#     """
#     global _DeepFace

#     if _DeepFace is None:
#         try:
#             from deepface import DeepFace
#             _DeepFace= DeepFace
#             logger.info("DeepFace imported successfully.")
#         except Exception:
#             logger.exception("Failed to import DeepFace.")
#             raise HTTPException(
#                 status_code=500,
#                 detail="Face recognition service is unavailable."
#             )
#     return _DeepFace

import traceback

def get_deepface():
    global _DeepFace

    if _DeepFace is None:
        try:
            from deepface import DeepFace
            _DeepFace = DeepFace
            return _DeepFace

        except Exception as e:
            print("\n" + "=" * 60)
            print("DEEPFACE IMPORT FAILED")
            print(f"Exception type: {type(e).__name__}")
            print(f"Exception: {e}")
            traceback.print_exc()
            print("=" * 60 + "\n")

            raise HTTPException(
                status_code=500,
                detail=str(e)   # TEMPORARY
            )

    return _DeepFace

def generate_embedding(image_bytes: bytes) -> List[float]:
    """
    Generates a facial embedding from an uploaded image.

    Args:
        image_bytes: Raw bytes of the uploaded image.

    Returns:
        A list of floats representing the facial embedding.
    """

    try:
        # convert bytes to image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(
                status_code=400,
                detail="Invalid image uploaded"
            )
        
        DeepFace= get_deepface()

        # generate embedding
        result = DeepFace.represent(
            img_path = img,
            model_name="Facenet",
            detector_backend="opencv",
            enforce_detection = True
        )

        if not result:
            raise HTTPException(
                status_code=400,
                detail="No face detected."
            )

        embedding = result[0]["embedding"]

        logger.info("Face embedding generated successfully.")

        return embedding
    
    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error while generating embedding")
        raise HTTPException(
            status_code=500,
            detail="Failed to generate face embedding"
        )