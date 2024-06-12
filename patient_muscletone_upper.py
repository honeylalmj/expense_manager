from kivy.lang import Builder
from kivymd.app import MDApp
from patient_muscletone_lower import PatientMuscletoneLower
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
        text: "Muscle tone test : Upper limb"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.58, "center_y": 0.8}
        size_hint: 0.3, 0.1
    MDLabel:
        text: "Shoulder :"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.5, "center_y": 0.7}
        size_hint: 0.3, 0.1
    MDTextField:
        id: shoulder_left_textfield
        hint_text: "Left"
        multiline: True
        pos_hint: {"center_x": 0.48, "center_y": 0.7}
        size_hint: 0.1, 0.1
    MDTextField:
        id: shoulder_right_textfield
        hint_text: "Right"
        multiline: True
        pos_hint: {"center_x": 0.6, "center_y": 0.7}
        size_hint: 0.1, 0.1
    MDLabel:
        text: "Elbow :"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.5, "center_y": 0.6}
        size_hint: 0.3, 0.1
    MDTextField:
        id: elbow_left_textfield
        hint_text: "Left"
        multiline: True
        pos_hint: {"center_x": 0.48, "center_y": 0.6}
        size_hint: 0.1, 0.1
    MDTextField:
        id: elbow_right_textfield
        hint_text: "Right"
        multiline: True
        pos_hint: {"center_x": 0.6, "center_y": 0.6}
        size_hint: 0.1, 0.1
    MDLabel:
        text: "Forearm :"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.3, 0.1
    MDTextField:
        id: forearm_left_textfield
        hint_text: "Left"
        multiline: True
        pos_hint: {"center_x": 0.48, "center_y": 0.5}
        size_hint: 0.1, 0.1
    MDTextField:
        id: forearm_right_textfield
        hint_text: "Right"
        multiline: True
        pos_hint: {"center_x": 0.6, "center_y": 0.5}
        size_hint: 0.1, 0.1
    MDLabel:
        text: "Wrist :"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        size_hint: 0.3, 0.1
    MDTextField:
        id: wrist_left_textfield
        hint_text: "Left"
        multiline: True
        pos_hint: {"center_x": 0.48, "center_y": 0.4}
        size_hint: 0.1, 0.1
    MDTextField:
        id: wrist_right_textfield
        hint_text: "Right"
        multiline: True
        pos_hint: {"center_x": 0.6, "center_y": 0.4}
        size_hint: 0.1, 0.1
    MDLabel:
        text: "Fingers :"
        theme_text_color: "Custom"
        text_color: "black"
        pos_hint: {"center_x": 0.5, "center_y": 0.3}
        size_hint: 0.3, 0.1
    MDTextField:
        id: fingers_left_textfield
        hint_text: "Left"
        multiline: True
        pos_hint: {"center_x": 0.48, "center_y": 0.3}
        size_hint: 0.1, 0.1
    MDTextField:
        id: fingers_right_textfield
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

class PatientMuscletoneUpper(MDApp):
    def __init__(self,patient_no,date,email, **kwargs):
        super().__init__(**kwargs)
        if getattr(sys, 'frozen', False):
            base_path = os.path.dirname(sys.executable)
        else:
            base_path = os.path.dirname(__file__)
        self.patient_json_file_path = os.path.join(base_path,'patient_data.json')
        self.patient = patient_no
        self.date = date
        self.email = email
        self.data = {}

    limb_textfield_ids = {
        "shoulder": ("shoulder_left_textfield", "shoulder_right_textfield"),
        "elbow": ("elbow_left_textfield", "elbow_right_textfield"),
        "forearm-Foot": ("forearm_left_textfield", "forearm_right_textfield"),
        "wrist": ("wrist_left_textfield", "wrist_right_textfield"),
        "fingers": ("fingers_left_textfield", "fingers_right_textfield")
    }

    def build(self):
        return Builder.load_string(KV)
    
    def save_file(self):
        try:
            with open(self.patient_json_file_path,'r')as file:
                existing_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            existing_data = {}
        patient_id = str(self.patient)
        email = self.email

        if email in existing_data and patient_id in existing_data[email]:
            existing_data[email][patient_id][self.date].update(self.data)  
        with open(self.patient_json_file_path,'w') as file :
            json.dump(existing_data,file, indent=2)
        file.close()  

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
            
            muscletone_upper = {}
            for limb, (left_id, right_id) in self.limb_textfield_ids.items():
                left_range = self.root.ids[left_id].text.strip()
                right_range = self.root.ids[right_id].text.strip()

                muscle_tone_upper_asess = {"Left": left_range,
                                            "Right": right_range}
                muscletone_upper[limb]=muscle_tone_upper_asess
                
            self.data['Muscle tone test for Upper limb'] = muscletone_upper
            self.save_file()
            print(self.data)
            self.stop() 
            PatientMuscletoneLower(self.patient,self.date,self.email).run()       
            
           

if __name__ == '__main__':
    PatientMuscletoneUpper().run()
