from fastapi import HTTPException
import cv2
import numpy as np
import logging
from typing import List

logger = logging.getLogger(__name__)

_face_app = None


def get_face_app():
    global _face_app

    if _face_app is None:
        try:
            from insightface.app import FaceAnalysis

            _face_app = FaceAnalysis(
                name="buffalo_l",
                providers=["CPUExecutionProvider"]
            )

            _face_app.prepare(
                ctx_id=0,
                det_size=(640, 640)
            )

            logger.info("InsightFace initialized successfully.")

        except Exception as e:
            logger.exception("Failed to initialize InsightFace")

            raise HTTPException(
                status_code=500,
                detail=f"Face recognition initialization failed: {str(e)}"
            )

    return _face_app


def generate_embedding(image_bytes: bytes) -> List[float]:

    try:

        nparr = np.frombuffer(image_bytes, np.uint8)

        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(
                status_code=400,
                detail="Invalid image uploaded."
            )

        app = get_face_app()

        faces = app.get(img)

        if len(faces) == 0:
            raise HTTPException(
                status_code=400,
                detail="No face detected."
            )

        if len(faces) > 1:
            raise HTTPException(
                status_code=400,
                detail="Multiple faces detected. Please upload an image with only one face."
            )

        embedding = faces[0].embedding.astype(np.float32)

        logger.info("Face embedding generated successfully.")

        return embedding.tolist()

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("Unexpected error while generating embedding")

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )