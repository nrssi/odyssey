import os
from kivymd.uix.screen import Screen
from kivymd.uix.card import MDCard
from kivymd.uix.fitimage import FitImage
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
        title_image_path = os.environ["VP_ROOT_DIR"] + \
            "/assets/UI/project_title.png"
        title_image = FitImage(source=title_image_path)
        uuid_input = MDTextField(
            hint_text="UUID",
            helper_text_mode="on_focus",
            size_hint=(1, None),
            height=50,
            pos_hint={"top": 0.5, "left": 0.5}
        )

        new_user_label = MDRectangleFlatButton(
            text="New User?",
            size_hint=(0.5, None),
            height=50
        )

        proceed_button = MDRectangleFlatButton(
            text="Proceed",
            size_hint=(0.5, None),
            height=50,
            on_press=self.new_user_callback
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
        card.add_widget(title_image)
        card.add_widget(uuid_input)
        card.add_widget(button_box)

        self.add_widget(card)

    def new_user_callback(self, _):
        self.manager.current = "register"
