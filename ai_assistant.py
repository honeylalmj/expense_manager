from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton, MDFlatButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivymd.uix.scrollview import MDScrollView
import requests
import json

# KV String defining the layout
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.screen = Builder.load_string(KV)

    def build(self):
        return self.screen

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
        if self.is_greeting(user_input):
            return "Hello! How can I assist you with your physiotherapy questions today?"
        
        try:
            # Define the URL for the API endpoint
            url = "http://localhost:11434/api/chat"
            
            # Define the initial prompt
            initial_prompt = "You are an AI specialized in physiotherapy. Only answer questions related to physiotherapy. If a question is not related to physiotherapy, politely refuse to answer."

            # Define the payload with initial instruction and user input
            payload = {
                "model": "gemma:2b",
                "messages": [
                    {"role": "system", "content": initial_prompt},
                    {"role": "user", "content": user_input}
                ]
            }
            
            # Send a POST request to the API
            response = requests.post(url, json=payload)

            # Split the response into individual JSON objects
            response_lines = response.content.strip().split(b'\n')

            # Initialize the AI response
            ai_response = ""

            # Iterate over each JSON object and parse it
            for line in response_lines:
                try:
                    json_obj = json.loads(line)
                    ai_response += json_obj["message"]["content"] + " "
                except Exception as e:
                    print("Error parsing JSON response:", e)

            # If no valid JSON object was found
            if not ai_response:
                print("Error: No valid JSON response found")
                return "Error: No valid JSON response found"
            
            return ai_response.strip()
        
        except Exception as e:
            print("Error:", e)
            return "Error: Exception occurred while getting AI response"
    
    def is_greeting(self, user_input):
        greetings = ["hi", "hello", "hey", "greetings", "good morning", "good afternoon", "good evening"]
        return any(greeting in user_input.lower() for greeting in greetings)

    def go_back(self):
        self.stop()
        from home_page import HomePage
        HomePage().run()

if __name__ == "__main__":
    ChatApp().run()
