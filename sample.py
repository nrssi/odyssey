from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image
from kivy.metrics import dp
from kivymd.uix.card import MDCard
from kivy.uix.relativelayout import RelativeLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.bottomnavigation import MDBottomNavigation, MDBottomNavigationItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from odyssey.blockchain import BlockChain
from odyssey.db_api import fetch_user


class TableTab(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Table Results"
        # Create the MDDataTable
        self.name = "table"
        bc = BlockChain()
        data = bc.get_votes()
        sorted_dict = dict(
            sorted(data.items(), key=lambda x: x[1], reverse=True))
        candidate_info = []
        for k in sorted_dict:
            candidate_info.append(fetch_user(int(k)))
        table = MDDataTable(
            check=False,
            elevation=0,
            use_pagination=True,
            size_hint=(None, None),
            height=400,
            width=600,
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            column_data=[("#", dp(10)), ("Candiate's Name", dp(50)),
                         ("Party Name", dp(30)), ("# of votes", dp(30))],
            row_data=[(str(i), k.name, "Party", sorted_dict[k.aadhar_number])
                      for i, k in enumerate(candidate_info, 1)]
        )

        # Add the table to the layout
        self.add_widget(table)


class ChartTab(MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        box = FloatLayout()
        box.pos_hint = {'center_x': 0.5, "center_y": 0.5}
        box.size_hint = (1, 1)
        card = MDCard(size_hint=(0.7, 0.7), orientation='vertical',
                      pos_hint={'center_x': 0.5, "center_y": 0.5})
        rel = RelativeLayout(pos_hint={'center_x': 0.5, "center_y": 0.5})
        self.text = "Pie chart"
        self.name = "pie"
        bc = BlockChain()
        data = bc.get_votes()
        sorted_dict = dict(
            sorted(data.items(), key=lambda x: x[1], reverse=True))
        candidate_info = []
        for k in sorted_dict:
            candidate_info.append(fetch_user(int(k)))
        data = [(k.name, sorted_dict[k.aadhar_number])
                for k in candidate_info]
        labels = [row[0] for row in data]
        votes = [row[1] for row in data]
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots()
        ax.pie(votes, labels=labels, autopct='%1.1f%%')
        # Add the chart to the layout
        rel.add_widget(FigureCanvasKivyAgg(plt.gcf()))
        card.add_widget(rel)
        box.add_widget(card)
        self.add_widget(box)


class CreditsTab(MDBoxLayout, MDBottomNavigationItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text = "Credits"
        # Create the circular layout
        self.name = "credits"
        circular_layout = MDBoxLayout(
            orientation='vertical',
            size_hint=(0.9, 0.9),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )

        # Add the label to the circular layout
        circular_layout.add_widget(
            MDLabel(
                text='Credits to Developers',
                font_style='H3',
                halign='center',
            )
        )

        # Add the circular layout to the layout
        self.add_widget(circular_layout)


class My(MDApp):
    def build(self):
        box = MDBoxLayout(orientation='horizontal')
        tabs = MDBottomNavigation(pos_hint={"center_x": 0.5,
                                            "center_y": 0.5})
        tabs.add_widget(TableTab())
        tabs.add_widget(ChartTab())
        tabs.add_widget(CreditsTab())
        box.add_widget(tabs)
        return box


My().run()
