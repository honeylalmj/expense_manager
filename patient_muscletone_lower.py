from kivy.lang import Builder
from kivymd.app import MDApp
from patient_funct_gait import PatientFunctGait
from pymongo import MongoClient
import os
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
        text: "Patient Assessment"
        theme_text_color: "Custom"
        text_color: "blue"
        pos_hint: {"center_x": 0.6,"center_y": 0.9}
        size_hint: 0.3, 0.1

    MDLabel:
        text: "Muscle tone test : Lower limb"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.58, "center_y": 0.8}
        size_hint: 0.3, 0.1
    MDLabel:
        text: "Hip :"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.5, "center_y": 0.7}
        size_hint: 0.3, 0.1
    MDTextField:
        id: hip_left_textfield
        hint_text: "Left"
        multiline: True
        pos_hint: {"center_x": 0.48, "center_y": 0.7}
        size_hint: 0.1, 0.1
    MDTextField:
        id: hip_right_textfield
        hint_text: "Right"
        multiline: True
        pos_hint: {"center_x": 0.6, "center_y": 0.7}
        size_hint: 0.1, 0.1
    MDLabel:
        text: "Knee :"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.5, "center_y": 0.6}
        size_hint: 0.3, 0.1
    MDTextField:
        id: knee_left_textfield
        hint_text: "Left"
        multiline: True
        pos_hint: {"center_x": 0.48, "center_y": 0.6}
        size_hint: 0.1, 0.1
    MDTextField:
        id: knee_right_textfield
        hint_text: "Right"
        multiline: True
        pos_hint: {"center_x": 0.6, "center_y": 0.6}
        size_hint: 0.1, 0.1
    MDLabel:
        text: "Ankle-Foot :"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.3, 0.1
    MDTextField:
        id: ankle_left_textfield
        hint_text: "Left"
        multiline: True
        pos_hint: {"center_x": 0.48, "center_y": 0.5}
        size_hint: 0.1, 0.1
    MDTextField:
        id: ankle_right_textfield
        hint_text: "Right"
        multiline: True
        pos_hint: {"center_x": 0.6, "center_y": 0.5}
        size_hint: 0.1, 0.1
    MDLabel:
        text: "Neck :"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        size_hint: 0.3, 0.1
    MDTextField:
        id: neck_left_textfield
        hint_text: "Left"
        multiline: True
        pos_hint: {"center_x": 0.48, "center_y": 0.4}
        size_hint: 0.1, 0.1
    MDTextField:
        id: neck_right_textfield
        hint_text: "Right"
        multiline: True
        pos_hint: {"center_x": 0.6, "center_y": 0.4}
        size_hint: 0.1, 0.1
    MDLabel:
        text: "Trunk :"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.5, "center_y": 0.3}
        size_hint: 0.3, 0.1
    MDTextField:
        id: trunk_left_textfield
        hint_text: "Left"
        multiline: True
        pos_hint: {"center_x": 0.48, "center_y": 0.3}
        size_hint: 0.1, 0.1
    MDTextField:
        id: trunk_right_textfield
        hint_text: "Right"
        multiline: True
        pos_hint: {"center_x": 0.6, "center_y": 0.3}
        size_hint: 0.1, 0.1  
    MDRaisedButton:
        text: "Next"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.5, "center_y": 0.2}
        size_hint: 0.1, 0.08
        on_press: app.next()                  
'''

class PatientMuscletoneLower(MDApp):

    def __init__(self,patient_no,date,email, **kwargs):
        super().__init__(**kwargs)
        mongo_uri = os.getenv('MONGODB_URI')
        self.client = MongoClient(mongo_uri)
        self.db = self.client['rehab']
        self.collection = self.db['patient_data']
        self.patient = patient_no
        self.date = date
        self.email = email

    limb_textfield_ids = {
        "Hip": ("hip_left_textfield", "hip_right_textfield"),
        "Knee": ("knee_left_textfield", "knee_right_textfield"),
        "Ankle-Foot": ("ankle_left_textfield", "ankle_right_textfield"),
        "Neck": ("neck_left_textfield", "neck_right_textfield"),
        "Trunk": ("trunk_left_textfield", "trunk_right_textfield")
    }

    def build(self):
        return Builder.load_string(KV)

    def set_error_message(self, instance_textfield, value):
        if not instance_textfield.text.strip():
            instance_textfield.error = True
            instance_textfield.helper_text = "Required field"
        else:
            instance_textfield.error = False
            instance_textfield.helper_text = ""

    def next(self):
        
        
        for limb, (left_id, right_id) in self.limb_textfield_ids.items():
            left_range = self.root.ids[left_id].text.strip()
            right_range = self.root.ids[right_id].text.strip()
            
            if not left_range:
                self.root.ids[left_id].error = True
                self.root.ids[left_id].helper_text = "Required field"
            else:
                self.root.ids[left_id].error = False
                self.root.ids[left_id].helper_text = ""
                
            if not right_range:
                self.root.ids[right_id].error = True
                self.root.ids[right_id].helper_text = "Required field"
            else:
                self.root.ids[right_id].error = False
                self.root.ids[right_id].helper_text = ""
        
        if (
           
             all(
                not self.root.ids[left_id].error and not self.root.ids[right_id].error
                for left_id, right_id in self.limb_textfield_ids.values()
            )
        ):
            
            muscletone_lower = {}
            for limb, (left_id, right_id) in self.limb_textfield_ids.items():
                left_range = self.root.ids[left_id].text.strip()
                right_range = self.root.ids[right_id].text.strip()
                muscle_tone_lower_asess = {"Left": left_range,
                                           "Right": right_range}
                muscletone_lower[limb] = muscle_tone_lower_asess

            key_email = self.email
            key_patient = self.patient
            key_date = self.date
            existing_document = self.collection.find_one({f"{key_email}.{key_patient}.{key_date}": {'$exists': True}})
            if existing_document :
                update = {
                    '$set': {
                        f"{key_email}.{key_patient}.{key_date}.Muscle tone test for Lower limb": muscletone_lower,
                        }
                }
                self.collection.update_one(
                    {f"{key_email}.{key_patient}.{key_date}": {'$exists': True}},
                    update,
                    upsert=True
                ) 
            self.stop()
            PatientFunctGait(self.patient,self.date,self.email).run()       
            
           

if __name__ == '__main__':
    PatientMuscletoneLower().run()
