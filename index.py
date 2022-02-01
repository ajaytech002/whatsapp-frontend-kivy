from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.list import TwoLineIconListItem
from kivymd.uix.list import ImageLeftWidget
from kivymd.uix.card import MDCard
from kivy.uix.modalview import ModalView
from kivy.uix.filechooser import FileChooserListView
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from kivy.properties import StringProperty, ObjectProperty
from kivymd.uix.behaviors import RoundedRectangularElevationBehavior
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.button import MDFlatButton, MDRaisedButton, MDRectangleFlatButton
from kivy.uix.dropdown import DropDown
from kivymd.uix.dialog import MDDialog
from kivymd.toast import toast
from kivymd.icon_definitions import md_icons
from kivymd.app import MDApp
from kivy.clock import Clock
import json
import os
from datetime import datetime

Builder.load_file("layouts/index.kv")
Builder.load_file("layouts/chat_bubble.kv")
Builder.load_file("layouts/profile_pic_dropdown.kv")


class MyGrid(Widget):
    pass


class ChatBubble(MDBoxLayout):
    msg = StringProperty()
    sender = StringProperty()
    pass


class ProfilePicDropDown(DropDown):
    pass


class IndexApp(MDApp):

    left_menu = ObjectProperty()
    dialog = None  # type: MDDialog

    def build(self):
        self.theme_cls.primary_palette = "Gray"
        self.theme_cls.accent_palette = "Blue"
        self.title = "Whatsapp"
        return MyGrid()

    def handle_left_menu(self, text):
        print(text)

    def handle_menu(self, *args):
        if (args[0] == "MENU_LEFT"):
            self.dropdown_left.open(args[1])
        if (args[0] == "MENU_RIGHT"):
            self.dropdown_right.open(args[1])

    def handle_menu_item(self, *args):
        if (args[0] == "Settings"):
            print("Settings")
        if (args[0] == "Logout"):
            print("Logout")
        if (args[0] == "Contact Info"):
            print("Contact Info")
        if (args[0] == "Close chat"):
            print("Close chat")
        if (args[0] == "Clear messages"):
            print("Clear messages")
        if (args[0] == "Delete chat"):
            print("Delete chat")

    def handle_file_chooser(self, *args):

        if (len(args[1]) == 0):
            return
        else:
            # some file has been selected.
            # check if its a png or jpeg
            file = args[1][0]
            file_name, file_extension = os.path.splitext(file)
            if (file_extension == ".png" or file_extension == ".jpeg"):
                # we have the right file. now we need to save it to the db.
                print("file_name = ", file_name)
                print("file_extension = ", file_extension)
                self.file_chooser_modal.dismiss()
                # Open the file
                # send the file to the server
            else:
                # we have the wrong file. let the user know via a toast
                toast("Please select a png or jpeg file")

    def create_modals(self):
        self.file_chooser_modal = ModalView(size_hint=(None, None),
                                            size=(400, 400), auto_dismiss=True)
        self.file_chooser = FileChooserListView()
        self.file_chooser.bind(selection=self.handle_file_chooser)
        self.file_chooser_modal.add_widget(self.file_chooser)

    '''Creates the left menu triggered by the 3 vertical dots on the left side of the toolbar
    '''

    def create_menus(self):
        self.dropdown_left = DropDown()
        self.dropdown_right = DropDown()
        # Kivy's DropDown's width is automatically set, based on the parent's width.
        # If you want to set it manually, you can do it like this:
        self.dropdown_left.auto_width = False
        self.dropdown_left.width = 200

        self.dropdown_right.auto_width = False
        self.dropdown_right.width = 200

        # There are 2 menu items at the moment.
        menu_items_left = ["Settings", "Logout"]
        menu_items_right = ["Contact Info", "Close chat",
                            "Clear messages", "Delete chat"]
        for item in menu_items_left:
            btn_settings = MDRaisedButton(
                text=item,
                size_hint_y=None,
                height=44,
                md_bg_color=get_color_from_hex("#f4f7f6"),
                text_color=get_color_from_hex("#424f49"),
                # size_hint_x=None,
                width="280dp",
                # increment_width="164dp",
                font_size="16sp",
            )
            btn_settings.bind(
                on_release=lambda btn: self.dropdown_left.select(btn.text))
            self.dropdown_left.add_widget(btn_settings)

        self.dropdown_left.bind(on_select=lambda instance,
                                x: self.handle_menu_item(x))

        for item in menu_items_right:
            # btn_settings = MDRaisedButton(
            #     text=item,
            #     size_hint_y=None,
            #     height=44,
            #     md_bg_color=get_color_from_hex("#f4f7f6"),
            #     text_color=get_color_from_hex("#424f49"),
            #     # size_hint_x=None,
            #     # width="280dp",
            #     # increment_width="200dp",
            #     font_size="16sp",
            # )

            btn_settings = Button(
                text=item,
                height=44,
                size_hint_y=None,
                background_color=get_color_from_hex("#ffffff"),
                background_normal="",
                color=get_color_from_hex("#536068"),
                # text_size=(200, None)
            )

            btn_settings.bind(
                on_release=lambda btn: self.dropdown_right.select(btn.text))
            self.dropdown_right.add_widget(btn_settings)

        self.dropdown_right.bind(on_select=lambda instance,
                                 x: self.handle_menu_item(x))

        # profile picture change dropdown.
        # self.profile_pic_dropdown = DropDown()
        # self.profile_pic_dropdown.add_widget(
        #     Button(text="Change Profile Picture", size_hint_y=None, height=44))
        # self.root.ids.profile_pic.bind(
        #     on_touch_down=lambda x, y: self.profile_pic_dropdown.open)

    # def open_profile_pic_dropdown(self, *args):
    #     print(args)
    #     self.profile_pic_dropdown.open(args[0])
    def open_profile_pic_selection(self, *args):
        print("open profile pic dropdown")

    def on_start(self):
        # Create the left and right menus
        self.create_menus()
        # self.profile_pic_dropdown = DropDown()
        # self.profile_pic_dropdown.add_widget(Button(text="Hello"))
        # self.root.ids.profile_pic.bind(
        #     on_touch_down=lambda x, y:  self.open_profile_pic_dropdown(x))

        self.create_modals()

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

    def change_name(self):
        name = self.root.ids.name.text
        print("name = ", name)
        ok_button = MDFlatButton(
            text="OK",
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
            on_release=lambda x: self.dialog.dismiss())
        if name == "":
            self.dialog = MDDialog(
                text="Your name can't be empty",
                buttons=[ok_button],
            )
            self.dialog.open()

    def change_status(self):
        status = self.root.ids.status.text
        ok_button = MDFlatButton(
            text="OK",
            theme_text_color="Custom",
            text_color=self.theme_cls.primary_color,
            on_release=lambda x: self.dialog.dismiss())
        if status == "":
            self.dialog = MDDialog(
                text="About can't be empty", buttons=[ok_button],)
            self.dialog.open()

    def update_profile_pic(self):
        print("hello")
        self.file_chooser_modal.open()


IndexApp().run()
