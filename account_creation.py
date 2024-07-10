import os
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
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
        text: "Account Creation"
        theme_text_color: "Custom"
        text_color: "blue"
        pos_hint: {"center_x": 0.6,"center_y": 0.9}
        size_hint: 0.3, 0.1

    MDTextField:
        id: text_field_firstname
        hint_text: "First name"
        mode: "rectangle"
        pos_hint: {"center_x": 0.35,"center_y": 0.8}
        size_hint: 0.25, 0.1

    MDTextField:
        id: text_field_lastname
        hint_text: "Last name"
        mode: "rectangle"
        pos_hint: {"center_x": 0.65,"center_y": 0.8}
        size_hint: 0.25, 0.1

    MDTextField:
        id: text_field_licensenumber
        hint_text: "License number"
        mode: "rectangle"
        pos_hint: {"center_x": 0.5, "center_y": 0.65}
        size_hint: 0.55, 0.1

    MDTextField:
        id: text_field_password
        hint_text: "Create password"
        mode: "rectangle"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.55, 0.1

    MDTextField:
        id: text_field_email
        hint_text: "Email id"
        mode: "rectangle"
        pos_hint: {"center_x": 0.5, "center_y": 0.35}
        size_hint: 0.55, 0.1

    MDRaisedButton:
        text: "Register"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.6, "center_y": 0.2}
        size_hint: 0.1, 0.08
        on_press: app.register()
    MDRaisedButton:
        text: "Back"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.4, "center_y": 0.2}
        size_hint: 0.1, 0.08
        on_press: app.back()    
'''

class AccountCreation(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        mongo_uri = os.getenv("MONGODB_URI")
        self.client = MongoClient(mongo_uri)
        self.db = self.client['rehab']
        self.collection = self.db['license']
        self.collection2 = self.db['user_data']
        self.initial_data = {
            "222": {
                "123": {
                    "first_name": "Jeeshma",
                    "last_name": "MJ"
                },
                "124": {
                    "first_name": "Honeylal",
                    "last_name": "MJ"
                },
                "125": {
                    "first_name": "Jayas",
                    "last_name": "Jacob"
                }
            }
        }
        self.check_and_insert_initial_data()

    def check_and_insert_initial_data(self):
        if not self.collection.find_one({"222": {"$exists": True}}):
            self.collection.insert_one({
                "222": self.initial_data["222"],
                "_id": ObjectId()
            })

    def back(self):
        self.stop()
        from login_page import LoginPage
        LoginPage().run()

    def show_license_exists_dialog(self):
        dialog = MDDialog(
            text="License number is valid, Sign Up Successful!",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.handle_license_exists_dialog_dismiss(dialog)
                )
            ]
        )
        dialog.open()

    def handle_license_exists_dialog_dismiss(self, dialog):
        dialog.dismiss()
        self.stop()
        from login_page import LoginPage
        LoginPage(self.screen.ids.text_field_licensenumber.text).run()

    def show_license_not_exists_dialog(self):
        dialog = MDDialog(
            text="ID number not recognized!",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: dialog.dismiss()
                )
            ]
        )
        dialog.open()

    def license_exists_dialog(self):
        dialog = MDDialog(
            text="Already registered!",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.handle_license_exists_dialog_dismiss(dialog)
                )
            ]
        )
        dialog.open()    

    def build(self):
        self.screen.ids.text_field_firstname.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )
        self.screen.ids.text_field_lastname.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )
        self.screen.ids.text_field_licensenumber.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )
        self.screen.ids.text_field_password.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )
        self.screen.ids.text_field_email.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )
        return self.screen

    def set_error_message(self, instance_textfield):
        if not instance_textfield.text.strip():
            instance_textfield.error = True
            instance_textfield.helper_text = "Required field"
        else:
            instance_textfield.error = False
            instance_textfield.helper_text = ""

    def register(self):
        first_name = self.screen.ids.text_field_firstname.text.capitalize()
        last_name = self.screen.ids.text_field_lastname.text.strip()
        license_number = self.screen.ids.text_field_licensenumber.text.strip()
        password = self.screen.ids.text_field_password.text.strip()
        email = self.screen.ids.text_field_email.text.strip()

        user_data = {
            "first_name": first_name,
            "last_name": last_name,
            "password": password,
            "email": email
        }

        self.screen.ids.text_field_firstname.error = False
        self.screen.ids.text_field_lastname.error = False
        self.screen.ids.text_field_licensenumber.error = False
        self.screen.ids.text_field_password.error = False
        self.screen.ids.text_field_email.error = False

        if not first_name:
            self.screen.ids.text_field_firstname.error = True
            self.screen.ids.text_field_firstname.helper_text = "Required field"

        if not last_name:
            self.screen.ids.text_field_lastname.error = True
            self.screen.ids.text_field_lastname.helper_text = "Required field"

        if not license_number:
            self.screen.ids.text_field_licensenumber.error = True
            self.screen.ids.text_field_licensenumber.helper_text = "Required field"

        if not password:
            self.screen.ids.text_field_password.error = True
            self.screen.ids.text_field_password.helper_text = "Required field"

        if not email:
            self.screen.ids.text_field_email.error = True
            self.screen.ids.text_field_email.helper_text = "Required field"

        if first_name and last_name and license_number and password and email:
            # Check if license number and first name exist in license collection
            license_record = self.collection.find_one({"222.{}".format(license_number): {"$exists": True}})
            if license_record and license_record["222"][license_number]["first_name"] == first_name:
                # Check if user data already exists in user_data collection
                user_data_exists = self.collection2.find_one({license_number: {"$exists": True}})
                if not user_data_exists:
                    # Insert new user data into user_data collection under the license number
                    self.collection2.insert_one({license_number: user_data})
                    self.show_license_exists_dialog()
                else:
                    self.license_exists_dialog()
            else:
                self.show_license_not_exists_dialog()

if __name__ == "__main__":
    AccountCreation().run()
