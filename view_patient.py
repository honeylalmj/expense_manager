from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.button import MDRaisedButton
import json
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.pickers import MDDatePicker
import os
import sys

KV = '''
FloatLayout:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1.0
        Rectangle:
            pos: self.pos
            size: self.size
    MDLabel:
        text: "View Patient"
        theme_text_color: "Custom"
        text_color: "blue"
        pos_hint: {"center_x": 0.62, "center_y": 0.8}
        size_hint: 0.3, 0.1
    MDTextField:
        id: patient_id
        hint_text: "Patient identification number"
        mode: "rectangle"
        pos_hint: {"center_x": 0.5, "center_y": 0.7}
        size_hint: 0.25, 0.1
    MDRaisedButton:
        id: date_button
        text: "Select Date"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        size_hint: 0.01, 0.01
        on_release: app.show_date_picker()
    MDRaisedButton:
        text: "Proceed"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.6, "center_y": 0.5}
        size_hint: 0.05, 0.05
        on_press: app.login()   
    MDRaisedButton:
        text: "Back"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.4, "center_y": 0.5}
        size_hint: 0.05, 0.05
        on_press: app.back()     
'''

class ViewPatientScreen(MDApp):
    
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
        self.screen.ids.date_button.bind(
            on_text=self.set_error_message,
        )
        return self.screen
    
    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()

    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)
        self.screen.ids.date_button.text = f' {value.strftime("%d-%m-%Y")}'

    def on_cancel(self, instance, value):
        pass    
    
    def read_file(self):
        try:
            with open(self.patient_json_file_path, 'r') as file:
                patient_data = json.load(file)
                return patient_data
        except (FileNotFoundError, KeyError, json.JSONDecodeError):
            print("Data not found")
            return {}      
  
    def set_error_message(self, instance_textfield):

        if not instance_textfield.text.strip():
            instance_textfield.error = True
            instance_textfield.helper_text = "Required field"
        else:
            instance_textfield.error = False
            instance_textfield.helper_text = ""
         

    def showlogin_exists__dialog(self, patient_id_no, consult_date, email_id):
        dialog = MDDialog(
            text="Patient ID and Consultation date exists !",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.handle_login_success_dialog_dismiss(dialog, patient_id_no, consult_date, email_id)
                )
            ]
        )
        dialog.open()
       

    def handle_login_success_dialog_dismiss(self, dialog, patient_id_no, consult_date, email):
        dialog.dismiss()
        MDApp.get_running_app().root.clear_widgets()
        from view_data import DisplayPatientDataApp
        DisplayPatientDataApp(patient_id_no, consult_date, email).run()
        
    def showlogin_not_exists_dialog(self):
        dialog = MDDialog(
            text="Entered Patient ID or Consultation date not exists !",
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
            text="Invalid entry !",
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

    def back(self):
        self.stop()
        from home_page import HomePage
        HomePage().run()

    def login(self):
        patient_info = self.read_file()
        patient_id_no = self.screen.ids.patient_id.text
        consult_date = self.screen.ids.date_button.text

        self.screen.ids.patient_id.error = False
        self.screen.ids.date_button.error = False

        if not patient_id_no:
            self.screen.ids.patient_id.error = True
            self.screen.ids.patient_id.helper_text = "Required field"

        if consult_date == "Select Date":
            self.screen.ids.date_button.error = True
            self.screen.ids.date_button.helper_text = "Required field"

        if (patient_id_no and (consult_date != "Select Date")) :
            email_ids = patient_info.keys()
            for email_id in email_ids:
                patient_data = patient_info[email_id]
                if patient_id_no in patient_data:
                    if consult_date in patient_data[patient_id_no]:
                        self.showlogin_exists__dialog(patient_id_no, consult_date,email_id)
                        return
            self.showlogin_not_exists_dialog()
        else:
            self.showlogin_not_exists_data_dialog()
if __name__ == '__main__':
    ViewPatientScreen().run()
