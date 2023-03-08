from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager

from .login import LoginScreen
from .register import RegisterScreen


class MyApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        screen_manager = ScreenManager()
        screen_manager.add_widget(RegisterScreen(name="register"))
        screen_manager.add_widget(LoginScreen(name="login"))
        return screen_manager
