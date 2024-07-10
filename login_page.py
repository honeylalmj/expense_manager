from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.icon_definitions import md_icons
from kivy.core.window import Window
from home_page import HomePage
from kivymd.uix.button import MDRaisedButton
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
KV = '''
FloatLayout:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1.0  # White background color (RGBA values)
        Rectangle:
            pos: self.pos
            size: self.size
    MDLabel:
        text: "Rehab Tracker"
        theme_text_color: "Custom"
        text_color: "blue"
        pos_hint: {"center_x": 0.6,"center_y": 0.8}
        size_hint: 0.3,0.1

    MDTextField:
        id: text_field_error
        hint_text: "Username or license number"
        mode: "rectangle"
        pos_hint: {"center_x": 0.5,"center_y": 0.7}
        size_hint: 0.5,0.1

    MDTextField:
        id: text_field_error1
        hint_text: "Enter Password"
        mode: "rectangle"
        password: True  # Set this property to True for password mode
        password_mask: "●"  # Optional: Set a custom character for the password mask
        pos_hint: {"center_x": 0.5, "center_y": 0.6}
        size_hint:0.5,0.1

    MDRaisedButton:
        text: "login"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.49, "center_y": 0.45}
        size_hint:0.12, 0.08
        on_press : app.login()

    MDRoundFlatButton:
        text: "Create new account"
        text_color: "black"
        pos_hint: {"center_x": 0.5, "center_y": 0.3}
        size_hint:0.3,0.1
        on_press :  app.create_account()
               
'''
DEFAULT_LOGIN_ID = None
class LoginPage(MDApp):
    def __init__(self,login_id = DEFAULT_LOGIN_ID, **kwargs):
        super().__init__(**kwargs)
        mongo_uri = os.getenv("MONGODB_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client['rehab']
        self.collection = self.db['user_data']
        self.screen = Builder.load_string(KV)
        self.login_id = login_id

    def on_start(self):
        if self.login_id != DEFAULT_LOGIN_ID:
            self.screen.ids.text_field_error.text = self.login_id
    
    def build(self):
        return self.screen


    def showlogin_exists__dialog(self):
        dialog = MDDialog(
            text="Login successful !",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.handle_login_success_dialog_dismiss(dialog)
                )
            ]
        )
        dialog.open()
    
    def handle_login_success_dialog_dismiss(self,dialog):
        dialog.dismiss()
        self.stop()
        HomePage().run()

    def showlogin_not_exists_dialog(self):
        dialog = MDDialog(
                text="Username or Password wrong !",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: dialog.dismiss()  # Add on_release function
                    ),
                ],
            )
        dialog.open()
    def showlogin_not_exists_data_dialog(self):
        dialog = MDDialog(
                text="User not exists,invalid entry !",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: dialog.dismiss()  # Add on_release function
                    ),
                ],
            )
        dialog.open()

    def login(self):
        username = self.screen.ids.text_field_error.text.strip()
        password = self.screen.ids.text_field_error1.text.strip()

        user_data = self.collection.find_one({username: {'$exists': True}})
    
        if user_data :
            if user_data[username]["password"] == password :
                self.showlogin_exists__dialog()
            else:
                self.showlogin_not_exists_dialog()
        else:
            self.showlogin_not_exists_data_dialog()

    def create_account(self) :
        self.stop()
        from account_creation import AccountCreation
        AccountCreation().run()



if __name__ == "__main__":
    LoginPage().run()