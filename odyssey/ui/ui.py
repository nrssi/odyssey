from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
import os
from .voterdetails import DetailScreen


from .login import WelcomeScreen
from .register import RegisterScreen


class BiometricVoting(MDApp):
    def build(self):
        self.data = {}
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        self.load_kv(f"{os.environ['VP_ASSETS_DIR']}/UI/login_layout.kv")
        screen_manager = ScreenManager()
        screen_manager.add_widget(WelcomeScreen(name="login"))
        screen_manager.add_widget(RegisterScreen(name="register"))
        screen_manager.add_widget(DetailScreen(name="details"))
        return screen_manager
