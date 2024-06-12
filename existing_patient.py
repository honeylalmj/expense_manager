from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from login_page import LoginPage
from kivymd.uix.button import MDRaisedButton
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
import json
from kivymd.uix.dialog import MDDialog
import os
import sys

KV = '''
FloatLayout:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1.0  # White background color (RGBA values)
        Rectangle:
            pos: self.pos
            size: self.size
    MDLabel:
        text: "Existing patient entry"
        theme_text_color: "Custom"
        text_color: "blue"
        pos_hint: {"center_x": 0.85, "center_y": 0.7}
        size_hint: 0.8, 0.8  # Adjusted size_hint
   
    MDTextField:
        id: patient_id
        hint_text: "Patient identification number"
        mode: "rectangle"
        pos_hint: {"center_x": 0.5,"center_y": 0.6}
        size_hint: 0.25, 0.1
    MDRaisedButton:
        text: "Proceed"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.05, 0.05
        on_press: app.login()    
'''

class ExistingPatient(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(__file__)
        self.patient_json_file_path = os.path.join(base_path,'patient_data.json')
        self.screen = Builder.load_string(KV)
        
    def build(self):

        self.screen.ids.patient_id.bind(
            on_text_validate=self.set_error_message,
            on_focus=self.set_error_message,
        )
        return self.screen
    
    def read_file(self):
        try:
            with open(self.patient_json_file_path,'r') as file :
                patient_data = json.load(file)
                return patient_data
        except (FileNotFoundError, KeyError,json.JSONDecodeError):
            print("Data not found")
            return {}      
  
    def set_error_message(self, instance_textfield):

        if not instance_textfield.text.strip():
            instance_textfield.error = True
            instance_textfield.helper_text = "Required field"
        else:
            instance_textfield.error = False
            instance_textfield.helper_text = ""

    def showlogin_exists__dialog(self,patient_id,email_id):
        dialog = MDDialog(
            text="Patient ID exists !",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.handle_login_success_dialog_dismiss(dialog,patient_id,email_id)
                )
            ]
        )
        dialog.open()
    
    def handle_login_success_dialog_dismiss(self,dialog,patient_no,email):

        dialog.dismiss()
        self.stop()
        from patient_assesment import PatientAssesment
        PatientAssesment(patient_no,email).run()
           
    def showlogin_not_exists_dialog(self):
        dialog = MDDialog(
                text="Entered Patient ID not exists !",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: dialog.dismiss()
                    ),
                ],
            )
        dialog.open()

    def showlogin_not_exists_data_dialog(self):
        dialog = MDDialog(
                text="No data available !",
                buttons=[
                    MDFlatButton(
                        text="OK",
                        theme_text_color="Custom",
                        text_color=self.theme_cls.primary_color,
                        on_release=lambda x: self.handle_login_unsuccess_dialog_dismiss(dialog)  # Add on_release function
                    ),
                ],
            )
        dialog.open()

    def handle_login_unsuccess_dialog_dismiss(self,dialog):
        dialog.dismiss()
        self.stop()
        from home_page import HomePage
        HomePage().run()

    def login(self):
        patient_existing_data = self.read_file()
        patient_id_no = self.screen.ids.patient_id.text.strip()

        self.screen.ids.patient_id.error = False

        if not patient_id_no:
            self.screen.ids.patient_id.error = True
            self.screen.ids.patient_id.helper_text = "Required field"
            
        if patient_existing_data :
            for email_id, patient_data in patient_existing_data.items():
                if patient_id_no in patient_data :
                    self.showlogin_exists__dialog(patient_id_no,email_id)
                    return
            self.showlogin_not_exists_dialog()  
        else:
            self.showlogin_not_exists_data_dialog()       
  
if __name__ == "__main__":
    ExistingPatient().run()