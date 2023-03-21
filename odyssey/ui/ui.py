from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from .voterdetails import DetailScreen


from .login import LoginScreen
from .register import RegisterScreen


class BiometricVoting(MDApp):
    def build(self):
        self.data = {}
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.primary_hue = '50'
        screen_manager = ScreenManager()
        screen_manager.add_widget(LoginScreen(name="login"))
        screen_manager.add_widget(RegisterScreen(name="register"))
        screen_manager.add_widget(DetailScreen(name="details"))
        return screen_manager
