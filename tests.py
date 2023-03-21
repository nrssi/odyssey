# import io
# import cv2
# import face_recognition
# from odyssey import db_api
# # from odyssey.auth import recognize_face
# from odyssey.db_models import Citizens
# db = db_api.SessionLocal()
# image_data = None
# with open("./assets/UI/project_title.png", "rb") as f:
#     image_data = f.read()
#
# user = Citizens(name="messi", address="messi", contact_ph=234,
#                 email="messi@goat", fingerprint=b"", face=image_data)
# db.add(user)
# db.commit()

# messi = db.query(Citizens).filter(Citizens.uuid == 10).first().face_features
# messi = face_recognition.load_image_file(io.BytesIO(messi))
# encoding = face_recognition.face_encodings(messi)[0]
# messi1 = face_recognition.load_image_file("./assets/Messi.jpg")
# encodings1 = face_recognition.face_encodings(messi1)[0]
# print(encoding-encodings1)
# result = recognize_face(image_data, messi)
# print(result)

# im = cv2.imread(io.BytesIO(image_data))


# fetcher user test

# print(db_api.fetch_user(6))
