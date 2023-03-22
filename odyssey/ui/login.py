from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.carousel import Carousel
from kivy.clock import Clock
import os


class QuotesCarousel(Carousel):

    def __init__(self, **kwargs):
        super(QuotesCarousel, self).__init__(**kwargs)
        self.interval = 3
        Clock.schedule_interval(self.load_next, self.interval)


class WelcomeScreen(MDScreen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)

    def new_user_callback(self):
        self.manager.current = "register"

    def proceed_button_callback(self):
        data = MDApp.get_running_app().data
        uuid_input = self.ids.uuid
        data["uuid"] = uuid_input.text
        self.manager.current = "details"
