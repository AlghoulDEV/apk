from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.dropdown import DropDown
from kivy.uix.recycleview import RecycleView

import sqlite3

class FriendApp(App):
    def build(self):
        self.connection = sqlite3.connect("friends_data.db")
        self.cursor = self.connection.cursor()
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Header ترحيبي
        header = Label(
            text="Welcome to Friend App 🐢",
            font_size=28,
            size_hint_y=None,
            height=50,
            bold=True
        )
        layout.add_widget(header)

        # أزرار
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        add_btn = Button(text="➕ Add Friend")
        view_btn = Button(text="📜 View Friends")
        btn_layout.add_widget(add_btn)
        btn_layout.add_widget(view_btn)
        
        layout.add_widget(btn_layout)

        add_btn.bind(on_press=self.add_friend)
        view_btn.bind(on_press=self.view_friends)

        return layout


    def add_friend(self, instance):
        # Popup form
        popup_layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        
        name_input = TextInput(hint_text="Name", multiline=False)
        nationality_input = TextInput(hint_text="Nationality", multiline=False)
        gender_input = Spinner(
            text="Select Gender",
            values=["Male ♂️", "Female ♀️", "BRO 💚"]
        )
        birth_year_input = TextInput(hint_text="Birth Year", multiline=False)
        phone_input = TextInput(hint_text="Phone", multiline=False)
        info_input = TextInput(hint_text="Info", multiline=True, size_hint_y=2)

        popup_layout.add_widget(name_input)
        popup_layout.add_widget(nationality_input)
        popup_layout.add_widget(gender_input)
        popup_layout.add_widget(birth_year_input)
        popup_layout.add_widget(phone_input)
        popup_layout.add_widget(info_input)

        save_btn = Button(text="Save", size_hint_y=None, height=40)
        cancel_btn = Button(text="Cancel", size_hint_y=None, height=40)

        btn_layout = BoxLayout(size_hint_y=None, height=40, spacing=10)
        btn_layout.add_widget(save_btn)
        btn_layout.add_widget(cancel_btn)

        popup_layout.add_widget(btn_layout)

        popup = Popup(title="Add New Friend", content=popup_layout, size_hint=(0.8, 0.8))
        
        def save_data(instance):
            self.cursor.execute("INSERT INTO FRIEND_INFO VALUES (?, ?, ?, ?, ?, ?)", (
                name_input.text,
                nationality_input.text,
                gender_input.text,
                int(birth_year_input.text) if birth_year_input.text.isdigit() else 0,
                phone_input.text,
                info_input.text
            ))
            self.connection.commit()
            popup.dismiss()
        
        save_btn.bind(on_press=save_data)
        cancel_btn.bind(on_press=lambda x: popup.dismiss())
        popup.open()

    def view_friends(self, instance):
        self.cursor.execute("SELECT * FROM FRIEND_INFO")
        data = self.cursor.fetchall()

        layout = BoxLayout(orientation='vertical', spacing=5, padding=5)

        # GridLayout للرؤوس والبيانات
        grid = GridLayout(cols=6, spacing=5, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        headers = ["Name", "Nationality", "Gender", "Birth Year", "Phone", "Info"]
        for h in headers:
            grid.add_widget(Label(text=h, bold=True, size_hint_y=None, height=30))

        for row in data:
            for item in row:
                grid.add_widget(Label(text=str(item), size_hint_y=None, height=30))

        # ScrollView لضمان تمرير البيانات
        scroll = ScrollView(size_hint=(1, 1))
        scroll.add_widget(grid)
        layout.add_widget(scroll)

        popup = Popup(title="Friends List", content=layout, size_hint=(0.9, 0.9))
        popup.open()


    def on_stop(self):
        self.connection.close()

if __name__ == "__main__":
    FriendApp().run()
