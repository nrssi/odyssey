from kivymd.uix import Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.textfield import MDTextField
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from ..db_api import register_user
from ..db_models import Citizens
import os
import io
import numpy as np
import cv2
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from ..fingerprint_bindings.pysgfplib import PYSGFPLib
from ..fingerprint_bindings.sgfdxdevicename import SGFDxDeviceName
from ..logger import logger
from ctypes import c_int, byref, c_char


class Camera(Image):
    def __init__(self, capture, fps, **kwargs):
        super(Camera, self).__init__(**kwargs)

        # Set up the capture object and frame dimensions
        self.capture = None
        self.width, self.height, self.frame = 0, 0, np.zeros((int(0), int(0)))
        self.is_captured = False
        # Set up the FPS clock
        self.fps = fps
        self.fps_clock: Clock = None

    def update(self, dt):
        # Read a frame from the camera
        ret, frame = self.capture.read()
        self.frame = frame
        if ret and not self.is_captured:
            # Convert the frame from BGR to RGB format
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create a Kivy texture from the frame
            texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')

            # Flip the frame vertically (for correct orientation)
            frame = cv2.flip(frame, 0)

            # Copy the frame into the texture
            texture.blit_buffer(
                frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

            # Set the texture as the source for the Image widget
            self.texture = texture

    def start(self):
        logger.info("Starting the Camera feed")
        self.capture = cv2.VideoCapture(0)
        self.fps_clock = Clock.schedule_interval(self.update, 1.0 / self.fps)

    def stop(self):
        # Stop the FPS clock and release the capture object
        logger.info("Stopping the Camera feed")
        self.fps_clock.cancel()
        self.capture.release()

    def get_frame(self):
        return self.frame


class FingerPrint(Image):
    def __init__(self, **kwargs):
        super(FingerPrint, self).__init__(**kwargs)
        self.fingerprint_data = np.zeros((300, 400))
        self.libobj = PYSGFPLib()
        self.frame = np.zeros((int(300), int(400)))
        self.is_loaded = False
        self.is_captured = False
        self.image_buffer = None
        logger.info("Creating PYSGFPLib context for fingerprint capture")
        self.libobj.Create()
        logger.info("Initializing PYSGFPLib object for fingerprint capture")
        self.libobj.Init(SGFDxDeviceName.SG_DEV_AUTO)

    def start(self):
        logger.info("Opening Device : 0 for capuring fingerprint")
        logger.info("Loading drivers for device : 0")
        self.libobj.OpenDevice(0)
        logger.info(
            "Actuating the device: 0, If this goes fine you should see LED blink")
        self.is_loaded = True
        self.fps_clock = Clock.schedule_interval(self.capture, 1/30)

    def stop(self):
        logger.info("Closing the device: 0")
        self.libobj.CloseDevice()
        self.fps_clock.cancel()

    def get_frame(self):
        return self.frame

    def capture(self, _):
        if not self.is_captured:
            cImageWidth = c_int(0)
            cImageHeight = c_int(0)
            self.libobj.GetDeviceInfo(
                byref(cImageWidth), byref(cImageHeight))
            image_buffer = (c_char*cImageWidth.value*cImageHeight.value)()
            self.libobj.GetImage(image_buffer)
            image_buffer = [[ord(b) for b in row] for row in image_buffer]
            img_array = np.array(image_buffer, dtype=np.uint8)
            img_array.reshape(cImageWidth.value, cImageHeight.value)
            img_array = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
            frame = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)

            # Create a Kivy texture from the frame
            texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')

            # Flip the frame vertically (for correct orientation)
            frame = cv2.flip(frame, 0)
            self.frame = frame
            # Copy the frame into the texture
            texture.blit_buffer(
                frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

            # Set the texture as the source for the Image widget
            self.texture = texture


class RegisterScreen(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)
        layout = MDGridLayout(cols=2)
        layout.spacing = 20
        layout.padding = [10, 0, 10, 0]
        biom_layout = MDBoxLayout(orientation="vertical",
                                  pos_hint={"center_x": 1, "center_y": 1},
                                  spacing=10, padding=[10, 10, 10, 10])
        details_layout = MDBoxLayout(
            orientation="vertical", spacing=10, padding=[0, 0, 20, 0])
        capture = cv2.VideoCapture(0)
        self.web_camera = Camera(capture=capture, fps=30)
        self.face_frame = np.zeros(
            (int(self.web_camera.width), int(self.web_camera.height)))
        self.finger_frame = None
        self.fingerprint_image = FingerPrint()
        self.capture_button = MDRectangleFlatButton(text="Capture", pos_hint={
            "center_x": 0.5, "center_y": 0.5}, on_release=self.capture_callback)
        self.read_button = MDRectangleFlatButton(text="Read", pos_hint={
            "center_x": 0.5, "center_y": 0.5}, on_release=self.fingerprint_callbak)
        biom_layout.add_widget(self.web_camera)
        biom_layout.add_widget(self.capture_button)
        biom_layout.add_widget(self.fingerprint_image)
        biom_layout.add_widget(self.read_button)

        register_gif_path = os.environ["VP_ROOT_DIR"] + \
            "/assets/UI/register.gif"
        self.registration_anim = Image(
            source=register_gif_path, anim_delay=0.04)
        self.name_input = MDTextField(hint_text="name", mode="rectangle")
        self.address_input = MDTextField(hint_text="address", mode="rectangle")
        self.father_name_input = MDTextField(
            hint_text="father's name", mode="rectangle")
        self.dob_input = MDTextField(
            hint_text="date of birth", mode="rectangle")
        self.email_input = MDTextField(hint_text="email", mode="rectangle")
        self.contact_ph_input = MDTextField(
            hint_text="contact number", mode="rectangle")
        self.register_button = MDRectangleFlatButton(
            text="Register", size_hint={1, None},
            on_release=self.register_button_callback)
        self.back_button = MDRectangleFlatButton(
            text="Back",
            on_release=self.back_button_callback,
            size_hint={1, None})
        details_layout.add_widget(self.registration_anim)
        details_layout.add_widget(self.name_input)
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
        _ = args  # Assigning this to remove the warnings
        self.web_camera.start()
        self.fingerprint_image.start()

    def on_leave(self, *args):
        _ = args  # Assigning this to remove the warnings
        print("debug")
        self.web_camera.stop()
        self.fingerprint_image.stop()

    def back_button_callback(self, _):
        self.manager.current = "login"

    def register_button_callback(self, _):
        name = self.name_input.text
        address = self.address_input.text
        father_name = self.father_name_input.text
        dob = self.dob_input.text
        email = self.email_input.text
        frame = self.face_frame
        frame = cv2.flip(frame, 0)
        _, frame_bytes = cv2.imencode('.jpg', frame)
        frame_bytes = frame_bytes.tobytes()
        face_file = io.BytesIO(frame_bytes)
        face_blob = face_file.read()
        finger_bytes = self.finger_frame
        finger_file = io.BytesIO(finger_bytes)
        finger_blob = finger_file.read()
        data = {"name": name, "address": address,
                "father_name": father_name, "dob": dob, "email": email, "face": face_blob, "fingerprint": finger_blob}
        citizen = Citizens(**data)
        register_user(citizen)
        self.manager.current = "login"

    def capture_callback(self, _):
        self.web_camera.is_captured = not self.web_camera.is_captured
        if self.web_camera.is_captured:
            self.face_frame = self.web_camera.get_frame()
            self.web_camera.stop()
            self.capture_button.text = "Recapture"
        else:
            self.web_camera.start()
            self.capture_button.text = "Capture"

    def fingerprint_callbak(self, _):
        self.fingerprint_image.is_captured = not self.fingerprint_image.is_captured
        if self.fingerprint_image.is_captured:
            self.finger_frame = self.fingerprint_image.get_frame()
            self.fingerprint_image.stop()
            self.read_button.text = "Recapture"
        else:
            self.fingerprint_image.start()
            self.read_button.text = "Capture"
