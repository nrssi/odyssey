from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.clock import Clock
import os

from .voterdetails import DetailScreen
from .login import WelcomeScreen
from .register import RegisterScreen
from .authenticate import AuthScreen
from .voting_page import VoteScreen
from .end_points import ThankYouScreen
from .end_points import SplashScreen


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
            f"{os.environ['VP_ASSETS_DIR']}/UI/layouts/end_points_layout.kv")
        self.screen_manager = ScreenManager()
        return self.screen_manager

    def on_start(self):
        self.sp = SplashScreen(name="splash")
        self.screen_manager.add_widget(self.sp)
        Clock.schedule_once(self.init_screens, 0)

    def init_screens(self, dt):
        self.screen_manager.add_widget(WelcomeScreen(name="login"))
        self.sp.ids.bar.value += 1
        Clock.schedule_once(self.load_details, 0)

    def load_details(self, dt):
        self.screen_manager.add_widget(DetailScreen(name="details"))
        self.sp.ids.bar.value += 1
        Clock.schedule_once(self.load_auth, 0)

    def load_auth(self, dt):
        self.screen_manager.add_widget(AuthScreen(name="auth"))
        self.sp.ids.bar.value += 1
        Clock.schedule_once(self.load_vote, 0)

    def load_vote(self, dt):
        self.screen_manager.add_widget(VoteScreen(name="vote"))
        self.sp.ids.bar.value += 1
        Clock.schedule_once(self.load_thanks, 0)

    def load_thanks(self, dt):
        self.screen_manager.add_widget(ThankYouScreen(name="thanks"))
        self.sp.ids.bar.value += 1
        Clock.schedule_once(self.load_registration, 0)

    def load_registration(self, dt):
        self.screen_manager.add_widget(RegisterScreen(name="register"))
        self.sp.ids.bar.value += 1
        if self.sp.ids.bar.value >= 6:
            self.screen_manager.current = "login"
