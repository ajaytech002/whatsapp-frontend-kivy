from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.list import TwoLineIconListItem
from kivymd.uix.list import ImageLeftWidget
from kivymd.uix.card import MDCard
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDRectangleFlatButton
from kivy.uix.dropdown import DropDown
from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivy.clock import Clock
import json
from datetime import datetime

Builder.load_file("layouts/index.kv")
Builder.load_file("layouts/chat_bubble.kv")


class MyGrid(Widget):
    pass


class ChatBubble(MDBoxLayout):
    msg = StringProperty()
    sender = StringProperty()
    pass


class IndexApp(MDApp):

    left_menu = ObjectProperty()

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.accent_palette = "Blue"
        self.title = "Whatsapp"
        return MyGrid()

    def handle_left_menu(self, text):
        print(text)

    def handle_menu(self, *args):
        if (args[0] == "LEFT_MENU"):
            self.dropdown.open(args[1])
            print(args[1])
            print("called")

    def handle_menu_item(self, *args):
        if (args[0] == "Settings"):
            print("Settings")
        if (args[0] == "Logout"):
            print("Logout")

    def on_start(self):
        # Create the left menu
        self.dropdown = DropDown()
        self.dropdown.auto_width = False
        self.dropdown.width = 200
        btn_settings = MDRaisedButton(
            text='Settings',
            size_hint_y=None,
            height=44,
            md_bg_color=get_color_from_hex("#f4f7f6"),
            text_color=get_color_from_hex("#424f49"),
            # size_hint_x=None,
            width="280dp",
            # increment_width="164dp",
            font_size="16sp",
        )
        # size_hint_y=None,
        # height=44,
        # background_color=get_color_from_hex(
        #     "#ffffff"),
        # background_normal="",
        # color=get_color_from_hex("#536068"),
        # )
        btn_settings.bind(
            on_release=lambda btn: self.dropdown.select(btn.text))
        self.dropdown.add_widget(btn_settings)

        btn_logout = Button(text="Logout",
                            size_hint_y=None,
                            height=44,
                            background_color=get_color_from_hex("#ffffff"),
                            background_normal="",
                            color=get_color_from_hex("#536068"),)
        btn_logout.bind(
            on_release=lambda btn: self.dropdown.select(btn.text))
        self.dropdown.add_widget(btn_logout)
        self.dropdown.bind(on_select=lambda instance,
                           x: self.handle_menu_item(x))

        # load chats
        chats = json.load(open("./data/chats.json"))
        for chat in chats["all"]:
            item = TwoLineIconListItem(
                text=chat["name"],
                secondary_text=chat["messages"][0]["message"],
            )
            item.bind(on_release=lambda x,
                      value=chat: self.display_chats(chat=value))
            item.add_widget(ImageLeftWidget(source="./images/profile.png"))
            self.root.ids.chats.add_widget(item)

    def display_chats(self, chat):
        self.root.ids.user_entered_msg.disabled = False
        id = chat["id"]

        # Get all the messages
        messages = chat["messages"]

        # Change the chat toolbar's (right side toolbar) title to the chat user's name
        self.root.ids.toolbar_chat.title = chat["name"]

        self.root.ids.chat.clear_widgets()

        # Add all the messages to the chat window
        for message in messages:
            self.root.ids.chat.add_widget(
                ChatBubble(
                    msg=message["message"], sender="YOU")
            )

    def send_user_entered_msg(self):
        print("message = ", self.root.ids.user_entered_msg.text)
        if (self.root.ids.user_entered_msg.text != ""):
            self.root.ids.chat.add_widget(
                ChatBubble(
                    msg=self.root.ids.user_entered_msg.text, sender="YOU")
            )
            # simulate an incoming chat also
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            self.root.ids.chat.add_widget(
                ChatBubble(
                    msg="response text", sender="ME")
            )
            # reset the text to blank
            self.root.ids.user_entered_msg.text = ""
            self.root.ids.user_entered_msg.focus = True
            Clock.schedule_once(self.focus_on_user_entered_msg)

    def focus_on_user_entered_msg(self, *args):
        self.root.ids.user_entered_msg.focus = True


IndexApp().run()
