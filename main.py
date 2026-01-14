
#!/usr/bin/env python3
"""
I Am Ironman - A Local Voice Assistant for your PC
Inspired by JARVIS from Iron Man
"""

import json
import os
import sys
import time
import threading
import speech_recognition as sr
import pyttsx3
from datetime import datetime
from secure_api_manager import SecureAPIManager, setup_api_key

class IronmanAssistant:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)
        self.config_file = 'data/config.json'
        self.assistant_name = None
        self.is_listening = False
        self.load_config()
        self.api_manager = SecureAPIManager()
        
    def load_config(self):
        """Load or create configuration file"""
        os.makedirs('data', exist_ok=True)
        
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                self.assistant_name = config.get('assistant_name')
        else:
            self.first_run_setup()
    
    def first_run_setup(self):
        """First run setup to get assistant name"""
        print("\n" + "="*60)
        print("🤖 I Am Ironman - First Time Setup")
        print("="*60)
        self.speak("Hey there, give me a name!")
        
        name = input("\n📝 Enter a name for your assistant: ").strip()
        
        if not name:
            name = "JARVIS"
            print(f"Using default name: {name}")
        
        self.assistant_name = name
        self.save_config()
        
        self.speak(f"Alright, I'm {name}. Pleasure to serve you, sir.")
        print(f"✅ Assistant configured as: {name}")

                # Setup API key for optional online features
        print("\n🔑 API Key Configuration")
        api_choice = input("Would you like to add an API key now? (y/n): ").lower()
        if api_choice == 'y':
            self.api_manager = setup_api_key()
        print()
        print("="*60 + "\n")
    
    def save_config(self):
        """Save configuration to file"""
        config = {
            'assistant_name': self.assistant_name,
            'created_at': datetime.now().isoformat(),
            'version': '1.0.0'
        }
        
        os.makedirs('data', exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def speak(self, text):
        """Text to speech"""
        print(f"🤖 {self.assistant_name}: {text}")
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"⚠️ TTS Error: {e}")
    

    def listen(self, timeout=10):
        """Listen for voice command"""
        try:
            with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1.0)
            self.recognizer.energy_threshold = 4000
            print("🎤 Listening...")               
            audio = self.recognizer.listen(source, timeout=timeout)

            text = self.recognizer.recognize_google(audio)
            print(f"👤 You: {text}")
            return text.lower()
        except sr.UnknownValueError:
            self.speak("Sorry, I didn't catch that.")
            return None
        except sr.RequestError:
            self.speak("Network error. Check your connection.")
            return None
        except Exception as e:
            if 'timed out' not in str(e).lower():
                print(f"⚠️ Error: {e}")
            return None
            
    def process_command(self, command):
        """Process voice commands"""
        # Application commands
        if 'chrome' in command or 'google' in command:
            self.speak("Opening Chrome")
            os.startfile('chrome.exe') if sys.platform == 'win32' else os.system('google-chrome &')
            return True
        
        elif 'vs code' in command or 'visual studio' in command:
            self.speak("Launching VS Code")
            os.startfile('code.exe') if sys.platform == 'win32' else os.system('code &')
            return True
        
        elif 'notepad' in command or 'text editor' in command:
            self.speak("Opening Notepad")
            os.startfile('notepad.exe') if sys.platform == 'win32' else os.system('gedit &')
            return True
        
        # Volume control
        elif 'increase volume' in command or 'volume up' in command:
            self.speak("Increasing volume")
            os.system('python -c "from ctypes import *; SetVolume(100)" 2>/dev/null || true')
            return True
        
        elif 'decrease volume' in command or 'volume down' in command:
            self.speak("Decreasing volume")
            return True
        
        elif 'mute' in command:
            self.speak("Muting")
            return True
        
        # Brightness control
        elif 'increase brightness' in command or 'brighten' in command:
            self.speak("Increasing brightness")
            return True
        
        elif 'decrease brightness' in command or 'dim' in command:
            self.speak("Decreasing brightness")
            return True
        
        # System commands
        elif 'time' in command:
            current_time = datetime.now().strftime("%H:%M")
            self.speak(f"The time is {current_time}")
            return True
        
        elif 'date' in command:
            current_date = datetime.now().strftime("%B %d, %Y")
            self.speak(f"Today is {current_date}")
            return True
        
        elif 'lock' in command or 'lock screen' in command:
            self.speak("Locking screen")
            os.system('rundll32.exe user32.dll,LockWorkStation' if sys.platform == 'win32' else 'gnome-screensaver-command -l')
            return True
        
        elif 'sleep' in command:
            self.speak("Going to sleep mode")
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0' if sys.platform == 'win32' else 'systemctl suspend')
            return True
        
        elif 'shutdown' in command or 'power off' in command:
            self.speak("Shutting down the system")
            os.system('shutdown /s /t 60' if sys.platform == 'win32' else 'shutdown -h +1')
            return True
        
        # Help
        elif 'help' in command or 'what can you do' in command:
            self.show_help()
            return True
        
        elif 'goodbye' in command or 'exit' in command or 'quit' in command:
            self.speak("Goodbye, sir. It was a pleasure.")
            return False
        
        return None
    
    def show_help(self):
        """Show available commands"""
        help_text = """
        Available Commands:
        
        📱 Applications:
          - Open Chrome / Google
          - Launch VS Code / Visual Studio
          - Open Notepad
        
        🔊 Volume:
          - Increase volume / Volume up
          - Decrease volume / Volume down
          - Mute / Unmute
        
        💡 Brightness:
          - Increase brightness / Brighten
          - Decrease brightness / Dim
        
        ⏰ System:
          - What time is it / Time
          - What's the date / Date
          - Lock screen
          - Sleep
          - Shutdown / Power off
        
        ℹ️ Other:
          - Help
          - Goodbye / Exit
        """
        print(help_text)
        self.speak("Here are my commands. Check the console for details.")
    
    def run(self):
        """Main assistant loop"""
        print("\n" + "="*60)
        print(f"🤖 {self.assistant_name} is ready!")
        print(f"Say '{self.assistant_name}' to wake me up")
        print("="*60 + "\n")
        
        self.is_listening = True
        
        while self.is_listening:
            try:
                command = self.listen()
                
                if not command:
                    continue
                
                if self.assistant_name.lower() in command:
                    self.speak("I'm here. What do you need?")
                    command = self.listen()
                    
                    if command:
                        result = self.process_command(command)
                        
                        if result is False:
                            self.is_listening = False
                        elif result is None:
                            self.speak("I'm not sure about that command.")
                
            except KeyboardInterrupt:
                print("\n\nShutting down...")
                self.speak("Goodbye, sir.")
                self.is_listening = False
            except Exception as e:
                print(f"⚠️ Error: {e}")
                time.sleep(1)

def main():
    """Main entry point"""
    try:
        assistant = IronmanAssistant()
        assistant.run()
    except Exception as e:
        print(f"Fatal Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
