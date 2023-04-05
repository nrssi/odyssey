# import cv2
# from odyssey import db_api
# from odyssey.auth import recognize_face
# from odyssey.db_api import fetch_user
# db = db_api.SessionLocal()
# image_data = None
# with open("/home/shashank/Downloads/profile.jpeg", "rb") as f:
#     image_data = f.read()
# user = fetch_user(3).face
# cap = cv2.VideoCapture(0)
# _, frame = cap.read()
# _, frame = cv2.imencode(".jpg", frame)
# print(recognize_face(user, frame.tobytes()))
# import cv2
# import sqlite3
# import numpy as np
# from kivy.app import App
# from kivy.graphics.texture import Texture
# from kivy.uix.image import Image as CoreImage
# from kivy.uix.boxlayout import BoxLayout
# from odyssey.db_api import fetch_user
#
#
# class MyApp(App):
#     def build(self):
#         # Connect to the SQLite database
#         # conn = sqlite3.connect('information.db')
#         # cursor = conn.cursor()
#         layout = BoxLayout()
#         # # Retrieve the JPEG image data from the database as a byte string
#         # cursor.execute("SELECT face FROM citizens WHERE uuid = ?", (3,))
#         # blob_data = cursor.fetchone()[0]
#         # Decode the byte string into a numpy array using cv2.imdecode()
#         user = fetch_user(3)
#         blob_data = user.face
#         bgr_img = cv2.imdecode(np.frombuffer(
#             blob_data, np.uint8), cv2.IMREAD_COLOR)
#         # Convert the numpy array from BGR to RGB format
#         rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
#         rgb_img = cv2.flip(rgb_img, 0)
#         # Create a Kivy texture from the RGB numpy array
#         texture = Texture.create(
#             size=(rgb_img.shape[1], rgb_img.shape[0]), colorfmt='rgb')
#         texture.blit_buffer(rgb_img.tobytes(),
#                             colorfmt='rgb', bufferfmt='ubyte')
#         # Create a Kivy image widget and set its texture
#         kivy_image = CoreImage()
#         kivy_image.texture = texture
#         layout.add_widget(kivy_image)
#         return layout
#
#
# if __name__ == '__main__':
#     MyApp().run()
from odyssey.db_api import fetch_user

print(fetch_user(878774689278))
