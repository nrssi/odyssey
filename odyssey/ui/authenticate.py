from kivy.uix.image import Image
from kivymd.uix.screen import Screen
import numpy as np
import cv2
from kivymd.app import MDApp
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from ..fingerprint_bindings.pysgfplib import PYSGFPLib
from ..fingerprint_bindings.sgfdxdevicename import SGFDxDeviceName
from ..logger import logger
from ctypes import c_int, byref, c_char
from ..auth import recognize_face
from ..db_api import fetch_user


class CameraFeed(Image):
    def __init__(self, **kwargs):
        super(CameraFeed, self).__init__(**kwargs)

        self.capture = None
        self.width, self.height, self.frame = 0, 0, np.zeros((int(0), int(0)))
        self.is_captured = False
        self.fps = 30
        self.fps_clock: Clock = None

    def update(self, dt):
        ret, frame = self.capture.read()
        self.frame = frame
        if ret and not self.is_captured:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')

            frame = cv2.flip(frame, 0)

            texture.blit_buffer(
                frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

            self.texture = texture

    def start(self):
        logger.info("Starting the Camera feed")
        self.capture = cv2.VideoCapture(0)
        self.fps_clock = Clock.schedule_interval(self.update, 1.0 / self.fps)

    def stop(self):
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

            texture = Texture.create(
                size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')

            frame = cv2.flip(frame, 0)
            self.frame = image_buffer
            texture.blit_buffer(
                frame.tobytes(), colorfmt='rgb', bufferfmt='ubyte')

            self.texture = texture


class AuthScreen(Screen):
    def on_enter(self):
        self.ids.fp.start()
        self.ids.cam.start()

    def face_authenticate(self):
        self.data = MDApp.get_running_app().data
        user = fetch_user(int(self.data["uuid"]))
        _, face_frame = cv2.imencode(".jpg", self.ids.cam.get_frame())
        result = recognize_face(face_frame, user.face)
        print(result)
