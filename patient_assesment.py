from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from patient_pain import PatientPain
from kivymd.uix.list import OneLineIconListItem
from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.pickers import MDDatePicker
import json
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
        text: "Patient Assessment"
        theme_text_color: "Custom"
        text_color: "blue"
        pos_hint: {"center_x": 0.6,"center_y": 0.9}
        size_hint: 0.3, 0.1        
    MDLabel:
        text: "Date :"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.4, "center_y": 0.8}
        size_hint: 0.3, 0.1
    MDRaisedButton:
        id: date_button
        text: "Select Date"
        pos_hint: {'center_x': 0.38, 'center_y': 0.8}
        size_hint: 0.01, 0.01
        on_release: app.show_date_picker()
        
    MDLabel:
        text: "Physical examination :"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.75, "center_y": 0.7}    
    MDTextField:
        id: textfield_physical
        multiline: True
        pos_hint: {"center_x": 0.5, "center_y": 0.6}
        size_hint: 0.5, 0.1
    MDLabel:
        text: "Pain assessment : "
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.4, "center_y": 0.5}
        size_hint: 0.3, 0.1

    MDSwitch:
        id: yes_switch
        on_active: app.toggle_textfield("Yes", self.active)
        pos_hint: {"center_x": 0.41, "center_y": 0.5}

    MDLabel:
        text: "Yes"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.3, 0.1

    MDSwitch:
        id: no_switch
        on_active: app.toggle_textfield("No", self.active)
        pos_hint: {"center_x": 0.51, "center_y": 0.5}

    MDLabel:
        text: "No"
        pos_hint: {"center_x": 0.6, "center_y": 0.5}
        size_hint: 0.3, 0.1

    MDTextField:
        id: assessment_textfield
        hint_text: "VAS between 0 - 10"
        multiline: True
        pos_hint: {"center_x": 0.425, "center_y": 0.4}
        size_hint: 0.35, 0.1    
    MDRaisedButton:
        text: "Next"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.6, "center_y": 0.2}
        size_hint: 0.1, 0.08
        on_press: app.next()

    MDRaisedButton:
        text: "Home"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.4, "center_y": 0.2}
        size_hint: 0.1, 0.08
        on_press: app.home()    
             
'''

class PatientAssesment(MDApp):
    def __init__(self,patient_id,email, **kwargs):
        super().__init__(**kwargs)
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(__file__)
        self.patient_json_file_path = os.path.join(base_path,'patient_data.json')
        self.screen = Builder.load_string(KV)
        self.patient = patient_id
        self.email = email
        self.data = {}


    def save_file(self):
        try:
            with open(self.patient_json_file_path, 'r') as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}

        patient_id = str(self.patient)
        email = self.email

        if email in existing_data and patient_id in existing_data[email]:
            date = self.data['Assessment']['Date']
            if date not in existing_data[email][patient_id]:
                existing_data[email][patient_id][date] = {}
            existing_data[email][patient_id][date].update(self.data)
        print(existing_data)


        with open(self.patient_json_file_path,'w') as file :
            json.dump(existing_data,file, indent=2)
        file.close() 

    def toggle_textfield(self, pain_assessment_type, switch_active):
        textfield = self.root.ids.assessment_textfield
        if pain_assessment_type == "Yes" and switch_active:
            textfield.disabled = False
            self.root.ids.no_switch.active = False
        elif pain_assessment_type == "No" and switch_active:
            textfield.disabled = True
            self.root.ids.yes_switch.active = False

    def on_save(self, instance, value, date_range):
        print(instance, value, date_range)
        self.screen.ids.date_button.text = f' {value.strftime("%d-%m-%Y")}'

    def on_cancel(self, instance, value):
        pass

    def show_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.on_save, on_cancel=self.on_cancel)
        date_dialog.open()
 

    def build(self):
        self.screen.ids.date_button.bind(
            on_text=self.set_error_message,
        )
        self.screen.ids.textfield_physical.bind(
            on_text=self.set_error_message, 
        )
        self.screen.ids.assessment_textfield.bind(
            on_text = self.set_error_message
        )
        
        return self.screen

    def set_error_message(self, instance_textfield, value=None):
        if not instance_textfield.text.strip() or (instance_textfield == self.screen.ids.drop_item and (value is None or value == "select")):
            instance_textfield.error = True
            instance_textfield.helper_text = "Required field"
        else:
            instance_textfield.error = False
            instance_textfield.helper_text = ""

    def nextpage(self,date):
        self.stop()
        PatientPain(self.patient,date,self.email).run()

    def home(self):
        self.stop()
        from home_page import HomePage
        HomePage().run()



    def next(self):
        
        date = self.screen.ids.date_button.text
        physical_examination = self.screen.ids.textfield_physical.text
        assessment_text = self.root.ids.assessment_textfield.text.strip()

        
        self.screen.ids.date_button.error = False
        self.screen.ids.textfield_physical.error = False


        if date == "Select Date":
            self.screen.ids.date_button.error = True
            self.screen.ids.date_button.helper_text = "Required field"

        if not physical_examination:
            self.screen.ids.textfield_physical.error = True
            self.screen.ids.textfield_physical.helper_text = "Required field"
            
        if self.root.ids.yes_switch.active and not assessment_text:
            self.root.ids.assessment_textfield.error = True
            self.root.ids.assessment_textfield.helper_text = "Required field"
        else:
            self.root.ids.assessment_textfield.error = False
            self.root.ids.assessment_textfield.helper_text = ""

        if (
            (date!= "Select Date")
            and physical_examination
            and (self.root.ids.yes_switch.active or self.root.ids.no_switch.active)
            and (self.root.ids.no_switch.active or (self.root.ids.yes_switch.active and assessment_text))
        ):
            if self.root.ids.no_switch.active:
                assessment_text = '0'
                print(f"Pain Assessment: {assessment_text}")
            else:
                print(f"Pain Assessment: {assessment_text}")
            
            assessment_data = {
                "Date": date,
                "Physical Examination": physical_examination,
            }
            print (assessment_data)
            self.data = {"Assessment": assessment_data}
            self.data['Pain assesment']= {'VAS value': assessment_text}

            
            print(self.data)
            self.save_file()
            self.nextpage(date)


            


if __name__ == "__main__":
    PatientAssesment().run()
