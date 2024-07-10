from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen
from patient_assesment import PatientAssesment
from kivymd.app import MDApp
import os
import sys
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
        text: "Patient details"
        theme_text_color: "Custom"
        text_color: "blue"
        pos_hint: {"center_x": 0.6,"center_y": 0.9}
        size_hint: 0.3, 0.1        
    MDLabel:
        text: "Patient Medical History :"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.75, "center_y": 0.7}

    MDTextField:
        id: past_textfield
        hint_text: "Enter Past Medical History"
        multiline: True
        pos_hint: {"center_x": 0.5, "center_y": 0.6}
        size_hint: 0.5, 0.1
         
    MDTextField:
        id: present_textfield
        hint_text: "Enter Present Medical History"
        multiline: True
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.5, 0.1

    MDRaisedButton:
        text: "Next"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.5, "center_y": 0.3}
        size_hint: 0.1, 0.08
        on_press: app.next()
             
'''

class PatientHistory(MDApp):
    def __init__(self,patient_id,email, **kwargs):
        super().__init__(**kwargs)
        mongo_uri = os.getenv('MONGODB_URI')
        self.client = MongoClient(mongo_uri)
        self.db = self.client['rehab']
        self.collection = self.db['patient_data']
        self.screen = Builder.load_string(KV)
        self.patient = patient_id
        self.email = email
        self.data = {}


    def on_cancel(self, instance, value):
        pass

    def build(self):
       
        self.screen.ids.past_textfield.bind(
            on_text=self.set_error_message,
        )
        self.screen.ids.present_textfield.bind(
            on_text=self.set_error_message, 
        )
        return self.screen

    def set_error_message(self, instance_textfield):
        if not instance_textfield.text.strip() :
            instance_textfield.error = True
            instance_textfield.helper_text = "Required field"
        else:
            instance_textfield.error = False
            instance_textfield.helper_text = ""

    def nextpage(self):
        self.stop()
        PatientAssesment(self.patient,self.email).run()

    def next(self):
        past_medical_history = self.screen.ids.past_textfield.text
        present_medical_history = self.screen.ids.present_textfield.text

        self.screen.ids.past_textfield.error = False
        self.screen.ids.present_textfield.error = False

        if not past_medical_history:
            self.screen.ids.past_textfield.error = True
            self.screen.ids.past_textfield.helper_text = "Required field"

        if not present_medical_history:
            self.screen.ids.present_textfield.error = True
            self.screen.ids.present_textfield.helper_text = "Required field"

        if past_medical_history and present_medical_history:

            key_email = self.email
            key_patient = self.patient
            key_personal_details = "Personal details"

            # Retrieve the existing document
            existing_document = self.collection.find_one({f"{key_email}.{key_patient}.{key_personal_details}": {'$exists': True}})
            
            # Merge new data with existing data
            if existing_document:
                update = {
                    '$set': {
                        f"{key_email}.{key_patient}.{key_personal_details}.Past Medical History": past_medical_history,
                        f"{key_email}.{key_patient}.{key_personal_details}.Present Medical History": present_medical_history
                        }
                }

            # Perform the update operation with upsert=True
                self.collection.update_one(
                    {f"{key_email}.{key_patient}.{key_personal_details}": {'$exists': True}},
                    update,
                    upsert=True
                )
                self.nextpage()

if __name__ == "__main__":
    PatientHistory().run()
