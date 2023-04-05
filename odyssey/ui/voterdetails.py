from kivymd.app import MDApp
from kivymd.uix import Screen
from kivy.graphics.texture import Texture
from kivy.uix.image import Image
import cv2
import numpy as np
from ..db_api import fetch_user


class DetailScreen(Screen):
    user_name = ""
    uuid = ""
    address = ""
    contact_ph = ""
    email = ""
    father_name = ""
    mother_name = ""
    dob = ""

    def __init__(self, **kw):
        super().__init__(**kw)

    def on_pre_enter(self, *args):
        self.data = MDApp.get_running_app().data
        user = fetch_user(int(self.data["uuid"]))
        self.ids.user_name.text = user.name
        self.ids.address.text = user.address
        self.ids.email.text = user.email
        self.ids.contact_ph.text = str(user.contact_ph)
        self.ids.mother_name.text = user.mother_name
        self.ids.father_name.text = user.father_name
        self.ids.uuid.text = str(user.aadhar_number)
        self.ids.dob.text = str(user.dob)
        self.ids.face_data.texture = self.get_blob_texture(user.face, True)
        self.ids.finger_data.texture = self.get_blob_texture(
            user.fingerprint, False)

    def get_blob_texture(self, blob, flip):
        bgr_img = cv2.imdecode(np.frombuffer(
            blob, np.uint8), cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        if flip:
            rgb_img = cv2.flip(rgb_img, 0)
        texture = Texture.create(
            size=(rgb_img.shape[1], rgb_img.shape[0]), colorfmt='rgb')
        texture.blit_buffer(rgb_img.tobytes(),
                            colorfmt='rgb', bufferfmt='ubyte')
        return texture
