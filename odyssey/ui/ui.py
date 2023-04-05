from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
import os
from .voterdetails import DetailScreen


from .login import WelcomeScreen
from .register import RegisterScreen
from .authenticate import AuthScreen
from .voting_page import VoteScreen
from .thankyou import ThankYouScreen


class BiometricVoting(MDApp):
    def build(self):
        self.data = {}
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Orange"
        self.load_kv(
            f"{os.environ['VP_ASSETS_DIR']}/UI/layouts/login_layout.kv")
        self.load_kv(
            f"{os.environ['VP_ASSETS_DIR']}/UI/layouts/register_layout.kv")
        self.load_kv(
            f"{os.environ['VP_ASSETS_DIR']}/UI/layouts/details_layout.kv")
        self.load_kv(
            f"{os.environ['VP_ASSETS_DIR']}/UI/layouts/auth_layout.kv")
        self.load_kv(
            f"{os.environ['VP_ASSETS_DIR']}/UI/layouts/voting_layout.kv")
        self.load_kv(
            f"{os.environ['VP_ASSETS_DIR']}/UI/layouts/thankyou_layout.kv")
        screen_manager = ScreenManager()
        screen_manager.add_widget(WelcomeScreen(name="login"))
        screen_manager.add_widget(RegisterScreen(name="register"))
        screen_manager.add_widget(DetailScreen(name="details"))
        screen_manager.add_widget(AuthScreen(name="auth"))
        screen_manager.add_widget(VoteScreen(name="vote"))
        screen_manager.add_widget(ThankYouScreen(name="thanks"))
        return screen_manager
