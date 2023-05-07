from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen
from kivy.graphics.texture import Texture
import cv2
from odyssey.blockchain import BlockChain
from kivymd.app import MDApp
import numpy as np


class MyScrollableList(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a GridLayout to hold the MDCard widgets
        self.grid = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        bc = BlockChain()
        data = bc.get_votes()
        sorted_dict = dict(
            sorted(data.items(), key=lambda x: x[1], reverse=True))
        print(sorted_dict)
        for k in sorted_dict:
            card = MDCard(size_hint_y=None, height='80dp',
                          padding=10, spacing=10, orientation='horizontal')

            # Add two MDLabel widgets to the card
            name_label = MDLabel(text=str(k),
                                 halign='left', valign='middle')
            party_label = MDLabel(
                text=str(data[k]), halign='left', valign='middle')
            card.add_widget(name_label)
            card.add_widget(party_label)

            # Add the MDCard widget to the GridLayout
            self.grid.add_widget(card)

        # Add the GridLayout to the ScrollView
        self.add_widget(self.grid)


class ResultScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Create a BoxLayout for the MainScreen with vertical orientation
        box_layout = BoxLayout(orientation='vertical')

        # Add a label to the top of the screen
        label = MDLabel(text="Results of the Poll",
                        halign='center', font_size=24, size_hint_y=None, height='120dp')
        box_layout.add_widget(label)

        # Add the MyScrollableList to the screen
        my_scrollable_list = MyScrollableList()
        box_layout.add_widget(my_scrollable_list)

        # Add the box layout to the screen
        self.add_widget(box_layout)


class ResultApp(MDApp):
    def build(self):
        return ResultScreen()


ResultApp().run()
