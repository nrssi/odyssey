from kivymd.app import MDApp
from kivymd.uix import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
import os
import io

from ..db_models import Citizens
from ..db_api import fetch_user


class DetailScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        data = MDApp.get_running_app().data
        voter_details: Citizens = None
        layout = MDGridLayout(cols=2)
        layout.spacing = 20
        layout.padding = [10, 0, 10, 0]
        # self.add_widget(layout)
        biom_layout = MDBoxLayout(orientation="vertical", pos_hint={
                                  "center_x": 1, "center_y": 1}, spacing=10, padding=[10, 10, 10, 10])
        details_layout = MDBoxLayout(orientation="vertical", spacing=10)
        self.image = Image(source=io.BytesIO(voter_details.face_features))
        fingerprint_image = Image(
            source="/home/shashank/Pictures/wallpapers/nixos.png")
        biom_layout.add_widget(fingerprint_image)

        register_gif_path = os.environ["VP_ROOT_DIR"] + \
            "/assets/UI/register.gif"
        self.registration_anim = Image(
            source=register_gif_path, anim_delay=0.04)
        name_input = MDTextField(hint_text="name", mode="rectangle")
        self.address_input = MDTextField(hint_text="address", mode="rectangle")
        self.father_name_input = MDTextField(
            hint_text="father's name", mode="rectangle")
        self.dob_input = MDTextField(
            hint_text="date of birth", mode="rectangle")
        self.email_input = MDTextField(hint_text="email", mode="rectangle")
        self.contact_ph_input = MDTextField(
            hint_text="contact number", mode="rectangle")
        self.register_button = MDRectangleFlatButton(
            text="Register", size_hint={1, None})
        self.back_button = MDRectangleFlatButton(
            text="Back", on_press=self.back_button_callback, size_hint={1, None})
        details_layout.add_widget(self.registration_anim)
        details_layout.add_widget(name_input)
        details_layout.add_widget(self.address_input)
        details_layout.add_widget(self.father_name_input)
        details_layout.add_widget(self.dob_input)
        details_layout.add_widget(self.email_input)
        details_layout.add_widget(self.back_button)
        details_layout.add_widget(self.register_button)
        layout.add_widget(biom_layout)
        layout.add_widget(details_layout)
        self.add_widget(layout)

    def on_enter(self, *args):
        self.web_camera.play = True

    def on_leave(self, *args):
        print("debug")
        self.web_camera.play = False

    def back_button_callback(self, _):
        self.manager.current = "login"
