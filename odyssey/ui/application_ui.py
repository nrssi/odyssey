from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.fitimage import FitImage
import os


class LoginLayout(MDCard):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint = (None, None)
        self.size = (400, 500)
        self.pos_hint = {"center_x": 0.5, "center_y": 0.5}

        self.orientation = "vertical"
        self.padding = [25, 25, 25, 40]

        self.uuid_input = MDTextField(
            hint_text="UUID",
            helper_text_mode="on_focus",
            size_hint=(1, None),
            height=50,
            pos_hint={"top": 0.5, "left": 0.5}
        )
        title_image_path = os.environ["VP_ROOT_DIR"] + \
            "/assets/UI/project_title.png"
        self.title_image = FitImage(source=title_image_path)
        self.new_user_label = MDRectangleFlatButton(
            text="New User?",
            size_hint=(0.5, None),
            height=50
        )

        self.proceed_button = MDRectangleFlatButton(
            text="Proceed",
            size_hint=(0.5, None),
            height=50
        )

        self.button_box = MDGridLayout(
            cols=2,
            size_hint=(1, None),
            height=50,
            padding=[0, 25, 0, 0]
        )

        self.button_box.add_widget(self.new_user_label)
        self.button_box.add_widget(self.proceed_button)

        self.add_widget(self.title_image)
        self.add_widget(self.uuid_input)
        self.add_widget(self.button_box)


class VotingApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        return LoginLayout()
