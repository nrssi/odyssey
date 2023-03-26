from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
import os
from .voterdetails import DetailScreen


from .login import WelcomeScreen
from .register import RegisterScreen
from .authenticate import AuthScreen


class BiometricVoting(MDApp):
    def build(self):
        self.data = {}
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        self.load_kv(f"{os.environ['VP_ASSETS_DIR']}/UI/login_layout.kv")
        self.load_kv(f"{os.environ['VP_ASSETS_DIR']}/UI/register_layout.kv")
        self.load_kv(f"{os.environ['VP_ASSETS_DIR']}/UI/details_layout.kv")
        self.load_kv(f"{os.environ['VP_ASSETS_DIR']}/UI/auth_layout.kv")
        screen_manager = ScreenManager()
        screen_manager.add_widget(WelcomeScreen(name="login"))
        screen_manager.add_widget(RegisterScreen(name="register"))
        screen_manager.add_widget(DetailScreen(name="details"))
        screen_manager.add_widget(AuthScreen(name="auth"))
        return screen_manager
