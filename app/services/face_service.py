from deepface import DeepFace
import numpy as np
import cv2

def generate_embedding(image_bytes):

    try:
        # convert bytes to image
        nparr = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # generate embedding
        result = DeepFace.represent(
            img_path = img,
            model_name = "ArcFace",
            enforce_detection = True
        )

        embedding = result[0]["embedding"]

        return embedding

    except Exception as e:
        return None