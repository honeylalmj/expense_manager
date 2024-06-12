from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
from openai import OpenAI

# Set up OpenAI client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

KV = '''
BoxLayout:
    orientation: 'vertical'
    
    MDScrollView:
        size_hint_y: 1
        MDLabel:
            id: chat_history
            text: ""
            halign: 'left'
            valign: 'top'
            markup: True
            padding: "10dp"
            size_hint_y: None
            height: self.texture_size[1] + dp(20)
    
    BoxLayout:
        size_hint_y: None
        height: "48dp"
        
        MDIconButton:
            icon: "send"
            on_press: app.send_message()
        
        MDTextField:
            id: user_input
            hint_text: "Type your message..."
            mode: "fill"
            fill_color: 1, 1, 1, 0.5
            on_text_validate: app.send_message()
    
    BoxLayout:
        size_hint_y: None
        height: "48dp"
        padding: "10dp"
        
        MDFlatButton:
            text: "Back"
            on_press: app.go_back()
'''

class ChatApp(MDApp):
    def build(self):
        return Builder.load_string(KV)
    
    def send_message(self):
        user_input = self.root.ids.user_input.text.strip()
        if user_input:
            # Add user message to chat history
            self.add_message(user_input, sent_by_user=True)
            # Send user input to AI
            ai_response = self.get_ai_response(user_input)
            # Add AI response to chat history
            self.add_message(ai_response, sent_by_user=False)
            # Clear user input field
            self.root.ids.user_input.text = ""
    
    def add_message(self, message, sent_by_user=True):
        chat_history_label = self.root.ids.chat_history
        if sent_by_user:
            message = "[color=008000]You:[/color] " + message
        else:
            message = "[color=0000FF]AI:[/color] " + message
        chat_history_label.text += "\n" + message
    
    def get_ai_response(self, user_input):
        # Initialize AI assistant instance
        assistant = client.chat.completions.create(
            model="local-model", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant for physiotherapy."},
                {"role": "user", "content": user_input}
            ]
        )
        
        # Access the message content from the completion object
        reply = assistant.choices[0].message.content
        
        return reply
    
    def go_back(self):
        self.stop()
        from home_page import HomePage
        HomePage().run()

if __name__ == "__main__":
    ChatApp().run()
