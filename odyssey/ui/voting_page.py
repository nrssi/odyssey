from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.button import MDFlatButton
from kivy.uix.image import AsyncImage
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics.texture import Texture
import cv2
from ..db_api import fetch_candidates
from ..blockchain import BlockChain
from kivymd.app import MDApp
import numpy as np


class MyScrollableList(ScrollView):
    def __init__(self, screen, **kwargs):
        super().__init__(**kwargs)

        # Create a GridLayout to hold the MDCard widgets
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        candidates = fetch_candidates()
        data = MDApp.get_running_app().data
        # Add MDCard widgets to the GridLayout
        i = 0
        for candidate in candidates:  # Replace 20 with the number of items you want to display
            card = MDCard(size_hint_y=None, height='180dp',
                          padding=10, spacing=10, orientation='horizontal')

            def printlam(x, id=candidate.aadhar_number):
                bc = BlockChain()
                bc.add_block({data['uuid']: id})
                bc.save_to_disk()
                screen.manager.current = 'login'
                pass

            # Add an AsyncImage widget to the card
            image = AsyncImage(size_hint_x=None, width='170dp', height='170dp')
            image.texture = self.get_blob_texture(candidate.face, True)
            card.add_widget(image)
            # Add two MDLabel widgets to the card
            name_label = MDLabel(text=candidate.name,
                                 halign='left', valign='middle')
            party_label = MDLabel(
                text=f'Representing Party {i} ', halign='left', valign='middle')
            i += 1
            card.add_widget(name_label)
            card.add_widget(party_label)

            # Add a MDFlatButton to the card
            vote_button = MDFlatButton(
                text='Vote', size_hint_x=None, width='60dp', pos_hint={'center_y': 0.5}, on_press=printlam, md_bg_color='#8ca9f5')
            card.add_widget(vote_button)

            # Add the MDCard widget to the GridLayout
            self.grid.add_widget(card)

        # Add the GridLayout to the ScrollView
        self.add_widget(self.grid)

    def get_blob_texture(self, blob, flip):
        bgr_img = cv2.imdecode(np.frombuffer(
            blob, np.uint8), cv2.IMREAD_COLOR)
        rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
        if flip:
            rgb_img = cv2.flip(rgb_img, 0)
        texture = Texture.create(
            size=(rgb_img.shape[1], rgb_img.shape[0]), colorfmt='rgb')
        texture.blit_buffer(rgb_img.tobytes(),
                            colorfmt='rgb', bufferfmt='ubyte')
        return texture


class VoteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a BoxLayout for the MainScreen with vertical orientation
        box_layout = BoxLayout(orientation='vertical')

        # Add a label to the top of the screen
        label = MDLabel(text="Pick Once\nYou can only pick one",
                        halign='center', font_size=24, size_hint_y=None, height='120dp')
        box_layout.add_widget(label)

        # Add the MyScrollableList to the screen
        my_scrollable_list = MyScrollableList(self)
        box_layout.add_widget(my_scrollable_list)

        # Add the box layout to the screen
        self.add_widget(box_layout)
