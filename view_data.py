from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from view_patient import ViewPatientScreen
import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
KV = '''
BoxLayout:
    orientation: 'vertical'
    ScrollView:
        MDBoxLayout:
            id: container
            orientation: 'vertical'
    FloatLayout:
        size_hint_y: None
        height: dp(50)  # Adjust the height of the FloatLayout if needed
        pos_hint: {"center_x": 0.5, "top": 0.98}  # Adjust the "top" value as needed

        MDRaisedButton:
            text: 'Back'
            size_hint: 0.07, 0.06
            pos_hint: {"center_x": 0.4855, "center_y": 0.5}
            on_press: app.back()
'''

class DisplayPatientDataApp(MDApp):
    def __init__(self, patient_id, consultation_date,email, **kwargs):
        super().__init__(**kwargs)
        mongo_uri = os.getenv('MONGODB_URI')
        self.client = MongoClient(mongo_uri)
        self.db = self.client['rehab']
        self.collection = self.db['patient_data']
        self.patient_id = patient_id
        self.consultation_date = consultation_date
        self.email = email


    def build(self):
        self.root = Builder.load_string(KV)
        self.display_data()
        return self.root

    def back(self):
        # Clear current widgets
        self.root.ids.container.clear_widgets()
        from view_patient import ViewPatientScreen
        ViewPatientScreen().run()

    def display_data(self):
        self.root.ids.container.clear_widgets()

        document = self.collection.find_one({self.email: {"$exists": True}})
        if document and self.patient_id in document[self.email] and self.consultation_date in document[self.email][self.patient_id]:
            patient_details = document[self.email][self.patient_id].get("Personal details", {})
            consultation_details = document[self.email][self.patient_id][self.consultation_date]

            assesment_details  = consultation_details.get("Assessment", {})
            pain_assesment = consultation_details.get("Pain assesment", {})
            upper_limb_motion = consultation_details.get("Range of motion for Upper limb", {})
            lower_limb_motion = consultation_details.get("Range of motion for Lower limb", {})
            muscle_test_upper_limb = consultation_details.get("Manual Muscle test for Upper limb", {})
            muscle_test_lower_limb = consultation_details.get("Manual Muscle test for Lower limb", {})
            muscle_tone_test_upper_limb = consultation_details.get("Muscle tone test for Upper limb", {})
            muscle_tone_test_lower_limb = consultation_details.get("Muscle tone test for Lower limb", {})
            functional_evaluation = consultation_details.get("Functional evaluation", {})
            gait_analysis = consultation_details.get("Gait anaylysis", {})
            activity = consultation_details.get("Activity limitations", {})
            treatment_plan = consultation_details.get("Treatment plan", {})
            treatment = consultation_details.get("Treatment", {})
            prognosis = consultation_details.get("Prognosis", {})
            

            if patient_details:
                data =''
                for main, sub_main in patient_details.items():
                    data += f"[b]{main}[/b] : {sub_main} "   
                self.add_rich_label("Personal details",data)
            else:
                self.add_label("No data available")

            if assesment_details:
                data=''
                for main, sub_main in assesment_details.items():
                        data += f"[b]{main}[/b] : {sub_main} "

                self.add_rich_label("Assesment details", data)
            else:
                self.add_label("No data available")
            if pain_assesment:
                data=''
                for main, sub_main in pain_assesment.items():
                        data += f"[b]{main}[/b] : {sub_main} "

                self.add_rich_label("Pain Assesment", data)
            else:
                self.add_label("No data available")    
            if upper_limb_motion:
                data=''
                for main, sub_main in upper_limb_motion.items():
                        data += f"[b]{main}[/b] : {sub_main} "

                self.add_rich_label("Range of motion of Upper limb", data)
            else:
                self.add_label("No data available")
            if lower_limb_motion:
                data=''
                for main, sub_main in lower_limb_motion.items():
                        data += f"[b]{main}[/b] : {sub_main} "

                self.add_rich_label("Range of motion of Lower limb", data)
            else:
                self.add_label("No data available")
            if muscle_test_upper_limb:
                data=''
                for main, sub_main in muscle_test_upper_limb.items():
                        data += f"[b]{main}[/b] : {sub_main} "

                self.add_rich_label("Manual muscle test for Upper limb", data)
            else:
                self.add_label("No data available")
            if muscle_test_lower_limb:
                data=''
                for main, sub_main in muscle_test_lower_limb.items():
                        data += f"[b]{main}[/b] : {sub_main} "

                self.add_rich_label("Manual muscle test for Lower limb", data)
            else:
                self.add_label("No data available")
            if muscle_tone_test_upper_limb:
                data=''
                for main, sub_main in muscle_tone_test_upper_limb.items():
                        data += f"[b]{main}[/b] : {sub_main} "

                self.add_rich_label("Muscle tone test for Upper limb", data)
            else:
                self.add_label("No data available")
            if muscle_tone_test_lower_limb:
                data=''
                for main, sub_main in muscle_tone_test_lower_limb.items():
                        data += f"[b]{main}[/b] : {sub_main} "

                self.add_rich_label("Muscle tone test for Lower limb", data)
            else:
                self.add_label("No data available")
            if functional_evaluation:
                data=''
                for main, sub_main in functional_evaluation.items():
                        data += f"[b]{main}[/b] : {sub_main} "

                self.add_rich_label("Functional evaluation", data)
            else:
                self.add_label("No data available")
            if gait_analysis:
                data=''
                for main, sub_main in gait_analysis.items():
                        data += f" {sub_main} "

                self.add_rich_label("Gait analysis", data)
            else:
                self.add_label("No data available")
            if activity:
                data=''
                for main, sub_main in activity.items():
                        data += f"[b]{main}[/b] : {sub_main} "

                self.add_rich_label("Activity", data)
            else:
                self.add_label("No data available")
            if treatment_plan:
                data=''
                for main, sub_main in treatment_plan.items():
                        data += f"[b]{main}[/b] : {sub_main} "

                self.add_rich_label("Treatment plan", data)
            else:
                self.add_label("No data available")
            if treatment:
                data=''
                for main, sub_main in treatment.items():
                        data += f" {sub_main} "

                self.add_rich_label("Treatment", data)
            else:
                self.add_label("No data available")
            if prognosis:
                data=''
                for main, sub_main in prognosis.items():
                        data += f" {sub_main} "

                self.add_rich_label("Prognosis", data)
            else:
                self.add_label("No data available")                                          
        else:
            self.add_label("Patient ID and consultation date not provided")

    def add_label(self, text):
        label = MDLabel(text=text, theme_text_color="Primary", font_style='Body1')
        self.root.ids.container.add_widget(label)

    def add_rich_label(self, category, data):
        rich_label = MDLabel(
            text=f"[color=#006400][b]{category}[/b][/color] : {data} ",
            theme_text_color="Primary",
            markup=True,
            line_height=1.1
        )
        self.root.ids.container.add_widget(rich_label)


if __name__ == '__main__':
    DisplayPatientDataApp().run()
