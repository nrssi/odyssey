from kivy.uix.image import Image
import cv2
from kivy.clock import Clock
from kivymd.uix.anchorlayout import AnchorLayout
from kivymd.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.label import MDLabel
from kivy.uix.screenmanager import Screen
from kivymd.uix.card import MDCard

from kivy.graphics.texture import Texture


class Camera(Image):
    def __init__(self, **kwargs):
        super(Camera, self).__init__(**kwargs)
        self.capture = cv2.VideoCapture(0)
        Clock.schedule_interval(self.update, 1.0 / 30.0)

    def update(self, dt):
        ret, frame = self.capture.read()
        if ret:
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
            self.texture = texture

    def stop(self):
        self.capture.release()
        Clock.unschedule(self.update)

    def click(self):
        _, frame = self.capture.read()
        frame = cv2.flip(frame, 0)
        return frame


class RegisterScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = BoxLayout(orientation='horizontal', padding=20)

        # Create a BoxLayout for the input fields
        input_layout = BoxLayout(
            orientation='vertical', size_hint=(1, 1), padding=[0, 0, 0, 0], spacing=10)

        # Create the text input fields
        name_input = MDTextField(hint_text='Name', mode="rectangle")
        dob_input = MDTextField(
            hint_text='DOB', mode="rectangle", validator='date', date_format="dd/mm/yyyy")
        father_input = MDTextField(hint_text="Father's Name", mode="rectangle")
        address_input = MDTextField(hint_text='Address', mode="rectangle")
        email_input = MDTextField(
            hint_text='Email', mode="rectangle", validator="email")
        contact_ph = MDTextField(
            hint_text="Contact Number", mode="rectangle", validator="phone")
        proceed_button = MDRectangleFlatButton(text="Proceed")
        # Add the input fields to the input_layout
        input_layout.add_widget(name_input)
        input_layout.add_widget(dob_input)
        input_layout.add_widget(father_input)
        input_layout.add_widget(address_input)
        input_layout.add_widget(email_input)
        input_layout.add_widget(contact_ph)
        input_layout.add_widget(proceed_button)
        root.add_widget(input_layout)
        self.add_widget(root)
