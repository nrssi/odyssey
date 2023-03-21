import os
from kivy.uix.image import Image
from kivymd.app import MDApp
from kivymd.uix.screen import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.gridlayout import MDGridLayout


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        card = MDCard(size_hint=(None, None), size=(400, 500),
                      pos_hint={"center_x": 0.5, "center_y": 0.5})
        card.orientation = "vertical"
        card.padding = [25, 25, 25, 40]
        title_gif_path = os.environ["VP_ROOT_DIR"] + \
            "/assets/UI/voting.gif"
        title_gif = Image(source=title_gif_path, anim_delay=0.04)
        self.uuid_input = MDTextField(
            hint_text="UUID",
            mode="rectangle",
            helper_text_mode="on_focus",
            size_hint=(1, None),
            height=50,
            pos_hint={"top": 0.5, "left": 0.5}
        )

        new_user_label = MDRectangleFlatButton(
            text="New User?",
            size_hint=(0.5, None),
            height=50,
            on_release=self.new_user_callback
        )

        proceed_button = MDRectangleFlatButton(
            text="Proceed",
            size_hint=(0.5, None),
            height=50,
            on_release=self.proceed_button_callback
        )

        button_box = MDGridLayout(
            cols=2,
            size_hint=(1, None),
            height=50,
            spacing=20,
            padding=[0, 20, 0, 0]
        )

        button_box.add_widget(new_user_label)
        button_box.add_widget(proceed_button)
        card.add_widget(title_gif)
        card.add_widget(self.uuid_input)
        card.add_widget(button_box)

        self.add_widget(card)

    def new_user_callback(self, _):
        self.manager.current = "register"

    def proceed_button_callback(self, _):
        data = MDApp.get_running_app().data
        data["uuid"] = self.uuid_input.text
        self.manager.current = "details"
