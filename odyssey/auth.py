import face_recognition
import io
from .logger import logger


def recognize_face(image1, image2):
    """
    This function takes 2 streams of bytes as input 
    these streams are converted to images by using load_image_file.
    Keep in mind that these files need to be in compatible shape
    you have to insert binary BLOB data into database and make sure to read it properly and 
    send data from database via image1 and live image via image2
    """
    logger.info("Loading the first image file...")
    first = face_recognition.load_image_file(io.BytesIO(image1))
    logger.info("Loading the second image file...")
    second = face_recognition.load_image_file(io.BytesIO(image2))
    try:
        logger.info("Calculating encodings for the image from database...")
        first_encodings = face_recognition.face_encodings(first)[0]
        logger.info("Calculating encodings for the live image...")
        second_encodings = face_recognition.face_encodings(second)[0]
    except IndexError:
        logger.error("No face found")
        return False
    logger.info("Comapring encodings for a face match...")
    result = face_recognition.compare_faces(
        [first_encodings], second_encodings)
    logger.info("Face match Success...")
    return result
