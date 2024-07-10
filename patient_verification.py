from kivy.lang import Builder
from kivymd.app import MDApp
from patient_history import PatientHistory
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFlatButton

KV = '''
FloatLayout:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1.0  # White background color (RGBA values)
        Rectangle:
            pos: self.pos
            size: self.size
    MDLabel:
        text: "Patient Verification"
        theme_text_color: "Custom"
        text_color: "blue"
        pos_hint: {"center_x": 0.6,"center_y": 0.9}
        size_hint: 0.3, 0.1        
    MDTextField:
        id: text_field_verification
        hint_text: "Verification code"
        mode: "rectangle"
        pos_hint: {"center_x": 0.5, "center_y": 0.65}
        size_hint: 0.55, 0.1
    MDTextField:
        id: text_field_patient_id
        hint_text: "Patient ID"
        mode: "rectangle"
        pos_hint: {"center_x": 0.5, "center_y": 0.55}
        size_hint: 0.55, 0.1
    MDRaisedButton:
        text: "Next"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.5, "center_y": 0.2}
        size_hint: 0.1, 0.08
        on_press: app.next()
'''

class PatientVerification(MDApp):
    def __init__(self,verification,patient_id,email, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        self.verification = verification
        self.patient_id = patient_id
        self.email = email
    

    def build(self):
        return self.screen


    def showverification_exists__dialog(self):
        dialog = MDDialog(
            text="Entered Verification code and Patient id is correct !",
            buttons=[
                MDRaisedButton(
                    text="OK",
                    on_release=lambda x: self.handle_verification_success_dialog_dismiss(dialog)
                )
            ]
        )
        dialog.open()
    
    def handle_verification_success_dialog_dismiss(self,dialog):
        dialog.dismiss()
        self.stop()
        PatientHistory(self.patient_id,self.email).run()

    def showverification_not_exists_dialog(self):
        dialog = MDDialog(
                text="Verification code or Patient id entered is wrong !",
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
    def next(self):
        verification = self.screen.ids.text_field_verification.text
        patient_id = self.screen.ids.text_field_patient_id.text
        if verification and patient_id: 
            if int(self.verification) ==  int(verification) and int(self.patient_id) ==  int(patient_id)  :
                self.showverification_exists__dialog()
                
            else :
                self.showverification_not_exists_dialog()
                    
if __name__ == "__main__":
    PatientVerification().run()
