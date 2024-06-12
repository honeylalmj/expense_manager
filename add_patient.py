from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog


KV = '''

FloatLayout:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1.0
        Rectangle:
            pos: self.pos
            size: self.size
    MDLabel:
        text: "Add Patient"
        theme_text_color: "Custom"
        text_color: "blue"
        pos_hint: {"center_x": 0.62, "center_y": 0.8}
        size_hint: 0.3, 0.1
    MDIcon:
        icon: "account-plus-outline"
        pos_hint: {"center_x": .5, "center_y": .7}
        font_size: "36sp"

    MDRaisedButton:
        text: "New entry"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.5, "center_y": 0.6}
        size_hint: 0.1, 0.08
        on_release: app.new_patient_login()
    MDRaisedButton:
        text: "Existing entry"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.1, 0.08
        on_release: app.existing_patient_login()    
    MDRaisedButton:
        text: "Back"
        md_bg_color: "skyblue"
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        size_hint: 0.1, 0.06
        on_release: app.go_back() 

'''



class AddPatient(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        

    def build(self):
        return Builder.load_string(KV)


    def new_patient_login(self):
        self.stop()
        from patient_personal_details import PatientPersonalDetails
        PatientPersonalDetails().run()

    def existing_patient_login(self):
        self.stop()
        from existing_patient import ExistingPatient
        ExistingPatient().run()

    def go_back(self):
        self.stop()
        from home_page import HomePage
        HomePage().run()

if __name__ == '__main__':
    AddPatient().run()
