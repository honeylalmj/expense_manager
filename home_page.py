from kivymd.app import MDApp
from kivy.lang import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRectangleFlatIconButton
from kivy.core.window import Window
import webbrowser

KV = '''
FloatLayout:
    canvas.before:
        Color:
            rgba: 1, 1, 1, 1.0  # White background color (RGBA values)
        Rectangle:
            pos: self.pos
            size: self.size
    MDLabel:
        text: "Home"
        theme_text_color: "Custom"
        text_color: "blue"
        pos_hint: {"center_x": 0.63,"center_y": 0.8}
        size_hint: 0.3,0.1        
    MDIcon:
        icon: "account-plus-outline"
        pos_hint: {"center_x": .5, "center_y": .7}
        font_size: "36sp"
    MDIcon:
        icon: "eye"
        pos_hint: {"center_x": .5, "center_y": .5}
        font_size: "36sp"
    MDRaisedButton:
        text: "Add patient"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.5, "center_y": 0.6}
        size_hint:0.1, 0.08
        on_press : app.add_patient_login()
    MDRaisedButton:
        text: "View Patient"
        md_bg_color: "green"
        pos_hint: {"center_x": 0.5, "center_y": 0.4}
        size_hint:0.1, 0.08
        on_press : app.view_patient_login()
    MDTextButton:
        text: "Contact Support"
        custom_color: "black"  
        pos_hint: {"center_x": 0.61, "center_y": 0.3}
        size_hint:0.3,0.1 
        on_release: app.send_email()          
    MDTextButton:
        text: "AI Support"
        custom_color: "black"  
        pos_hint: {"center_x": 0.625, "center_y": 0.25}
        size_hint:0.3,0.1
        on_press: app.ai_api()          

        '''

class HomePage(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)
        
        
    def build(self):
        return self.screen
    
    def add_patient_login(self) :
        self.stop()
        from add_patient import AddPatient
        AddPatient().run()

    def view_patient_login(self):
        self.stop()
        from view_patient import ViewPatientScreen
        ViewPatientScreen().run()
         
    def send_email(self):
        default_email_address = "trackerrehab@gmail.com"
        webbrowser.open(f"mailto:{default_email_address}?subject=Support%20Required&body=Email%20body%20text")
    
    def ai_api(self):
        self.stop()
        from ai_assistant import ChatApp
        ChatApp().run()


if __name__ == "__main__":
    HomePage().run()