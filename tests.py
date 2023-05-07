from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.datatables import MDDataTable


class MainScreen(BoxLayout):
    data_table = ObjectProperty()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.data_table = MDDataTable(
            size_hint=(0.9, 0.6),
            column_data=[
                ("Key", 0.2),
                ("Value", 0.2),
            ],
            sorted_on="Value",
            rows_num=10,
        )
        self.add_widget(self.data_table)
        self.populate_table()

    def populate_table(self):
        data_dict = {"Apple": 10, "Banana": 5,
                     "Cherry": 7, "Durian": 3, "Eggplant": 9}
        data = []
        for key, value in sorted(data_dict.items(), key=lambda x: x[1], reverse=True):
            data.append((key, value))
        self.data_table.row_data = data


class DemoApp(MDApp):
    def build(self):
        return Builder.load_string(
            """
MainScreen:
"""
        )


if __name__ == "__main__":
    DemoApp().run()
