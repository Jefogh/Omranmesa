import base64
import random
import time
import asyncio
import threading
import cv2
import numpy as np
from PIL import Image
import httpx
import easyocr
import re
import json
import os
from io import BytesIO
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image as KivyImage
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.dialog import Dialog

# تحسين إعدادات EasyOCR لتسريع العملية
reader = easyocr.Reader(['en'], gpu=True, model_storage_directory=os.path.join(os.getcwd(), "model"), download_enabled=True)

class CaptchaApp(App):
    def build(self):
        self.accounts = {}
        self.background_images = []
        self.last_status_code = None
        self.last_response_text = None
        self.corrections = self.load_corrections()

        layout = BoxLayout(orientation='vertical')

        self.add_account_button = Button(text="Add Account")
        self.add_account_button.bind(on_press=self.add_account)
        layout.add_widget(self.add_account_button)

        self.upload_background_button = Button(text="Upload Backgrounds")
        self.upload_background_button.bind(on_press=self.upload_backgrounds)
        layout.add_widget(self.upload_background_button)

        self.account_column = BoxLayout(orientation='vertical')
        layout.add_widget(self.account_column)

        return layout

    async def upload_backgrounds(self, instance):
        """Upload background images for processing."""
        # Using Kivy FileChooser
        filechooser = FileChooserIconView()
        filechooser.filters = ['*.jpg', '*.png', '*.jpeg']
        filechooser.bind(on_submit=self.on_file_selection)
        
        # Display the file chooser
        popup = Popup(title="Select Background Images", content=filechooser, size_hint=(0.9, 0.9))
        popup.open()

    def on_file_selection(self, filechooser, selection, *args):
        """Handle the file selection."""
        if selection:
            self.background_images = [cv2.imread(file) for file in selection]
            self.show_message("Success", f"{len(self.background_images)} background images uploaded successfully!")

    def add_account(self, instance):
        """Add a new account for captcha solving."""
        # Implement account addition logic with Kivy dialogs
        pass  # Add your logic for user input dialogs

    def create_account_ui(self, username):
        """Create the UI elements for a specific account."""
        # Implement account UI creation logic with Kivy widgets
        pass  # Add your logic for account-specific UI

    async def request_captcha(self, username, captcha_id):
        """Request a captcha image for processing."""
        session = self.accounts[username].get('session')
        if not session:
            self.show_message("Error", f"No session found for user {username}")
            return

        # Implement captcha request logic
        pass  # Add your logic for requesting captcha

    def show_captcha(self, captcha_data, username, captcha_id):
        """Display the captcha image for user input using Kivy."""
        try:
            captcha_base64 = captcha_data.split(",")[1] if ',' in captcha_data else captcha_data
            captcha_image_data = base64.b64decode(captcha_base64)

            with open("captcha.jpg", "wb") as f:
                f.write(captcha_image_data)

            captcha_image = cv2.imread("captcha.jpg")
            processed_image = self.process_captcha(captcha_image)
            processed_image = cv2.resize(processed_image, (110, 60))
            processed_image[np.all(processed_image == [0, 0, 0], axis=-1)] = [255, 255, 255]
            _, encoded_image = cv2.imencode('.jpg', processed_image)
            encoded_image_str = base64.b64encode(encoded_image).decode('utf-8')

            # Create Kivy image
            kivy_image = KivyImage(source='data:image/jpeg;base64,' + encoded_image_str)

            # Implement Kivy layout for captcha image and input fields
            pass  # Add your logic for displaying captcha

        except Exception as e:
            self.show_message("Error", f"Failed to show captcha: {e}")

    def show_message(self, title, message):
        """Display a message dialog."""
        content = Label(text=message)
        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        popup.open()

    def process_captcha(self, captcha_image):
        """Apply advanced image processing to remove the background using added backgrounds while keeping original colors."""
        # Process captcha image
        pass  # Add your image processing logic

    @staticmethod
    def remove_background_keep_original_colors(captcha_image, background_image):
        """Remove background from captcha image while keeping the original colors of elements."""
        pass  # Add your background removal logic

    def submit_captcha(self, username, captcha_id, captcha_solution):
        """Submit the captcha solution to the server."""
        session = self.accounts[username].get('session')
        if not session:
            self.show_message("Error", f"No session found for user {username}")
            return

        # Implement captcha submission logic
        pass  # Add your logic for submitting captcha

    @staticmethod
    def generate_headers(user_agent):
        """Generate HTTP headers for the session."""
        return {
            'User-Agent': user_agent,
            'Content-Type': 'application/json',
            'Source': 'WEB',
            'Accept': 'application/json, text/plain, */*',
            'Referer': 'https://ecsc.gov.sy/',
            'Origin': 'https://ecsc.gov.sy',
            'Connection': 'keep-alive',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-site'
        }

    @staticmethod
    def generate_user_agent():
        """Generate a random user agent string."""
        user_agent_list = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv=89.0) Gecko/20100101 Firefox/89.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) "
            "Version/13.1.1 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/56.0.2924.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/47.0.2526.106 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
        ]
        
        return random.choice(user_agent_list)

    def correct_and_highlight(self, predictions, image):
        """Correct OCR predictions and apply color highlights to numbers and operators."""
        corrections = {
            'O': '0', 'S': '5', 'I': '1', 'B': '8', 'G': '6',
            'Z': '2', 'T': '7', 'A': '4', 'X': '*', '×': '*', 'L': '1',
            'H': '8', '_': '-', '/': '7', '£': '8', '&': '8'
        }

        # Prepare to highlight extracted numbers and operators in different colors
        num_color = (0, 255, 0)  # Green for numbers
        op_color = (0, 0, 255)  # Red for operators
        corrected_text = ""
        
        for text in predictions:
            text = text.strip().upper()
            for char in text:
                corrected_char = corrections.get(char, char)
                if corrected_char.isdigit():
                    corrected_text += corrected_char
                elif corrected_char in "+-*xX×":
                    corrected_text += corrected_char
                else:
                    corrected_text += corrected_char  # Non-highlighted

        return corrected_text, image

    def learn_from_correction(self, original_text, corrected_text):
        """Learn from user correction and store it."""
        corrections = self.load_corrections()
        corrections[original_text] = corrected_text
        self.save_corrections(corrections)

    def load_corrections(self):
        """Load corrections from a JSON file."""
        if os.path.exists("corrections.json"):
            with open("corrections.json", "r") as file:
                return json.load(file)
        return {}

    def save_corrections(self, corrections):
        """Save corrections to a JSON file."""
        with open("corrections.json", "w") as file:
            json.dump(corrections, file)

if __name__ == "__main__":
    CaptchaApp().run()

