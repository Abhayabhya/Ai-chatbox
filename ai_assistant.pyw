# Python AI Assistant Chatbox (with Voice Control)
#
# --- Installation ---
# Before running, you need to install some libraries. Open your terminal and run:
# pip install SpeechRecognition PyAudio wikipedia-api requests pyjokes
#
import tkinter as tk
from tkinter import scrolledtext, messagebox
import webbrowser
from datetime import datetime
import os
import requests
import wikipediaapi
import pyjokes
import speech_recognition as sr
import threading

class AssistantApp:
    def __init__(self, master):
        self.master = master
        master.title("AI Assistant")
        master.geometry("450x600")
        master.configure(bg="#2c3e50")

        self.wiki_wiki = wikipediaapi.Wikipedia('MyAssistant/1.0 (example@example.com)', 'en')

        self.chat_area = scrolledtext.ScrolledText(master, state='disabled', wrap=tk.WORD,
                                                   bg="#34495e", fg="#ecf0f1",
                                                   font=("Helvetica", 11))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.msg_entry = tk.Entry(master, font=("Helvetica", 12), bg="#ecf0f1")
        self.msg_entry.pack(padx=10, pady=(0, 5), fill=tk.X, expand=True)
        self.msg_entry.bind("<Return>", self.send_message)
        self.msg_entry.focus()

        # Frame for buttons
        button_frame = tk.Frame(master, bg="#2c3e50")
        button_frame.pack(padx=10, pady=(0, 10))

        self.send_button = tk.Button(button_frame, text="Send", command=self.send_message,
                                     bg="#2980b9", fg="white", font=("Helvetica", 10, "bold"),
                                     relief=tk.FLAT, width=10)
        self.send_button.pack(side=tk.LEFT, padx=5)

        self.listen_button = tk.Button(button_frame, text="Listen 🎤", command=self.start_listening_thread,
                                     bg="#16a085", fg="white", font=("Helvetica", 10, "bold"),
                                     relief=tk.FLAT, width=10)
        self.listen_button.pack(side=tk.LEFT, padx=5)

        self.add_message("AI: Hello! Main aapki kya sahayata kar sakta hoon? (Listen button try karein!)")

    def start_listening_thread(self):
        """Starts the listening process in a new thread to keep the GUI responsive."""
        threading.Thread(target=self.listen_command, daemon=True).start()

    def listen_command(self):
        """Listens for a voice command from the user."""
        r = sr.Recognizer()
        with sr.Microphone() as source:
            self.add_message("AI: Sun रहा हूँ...")
            self.listen_button.config(state=tk.DISABLED, text="Listening...")
            try:
                r.pause_threshold = 1
                audio = r.listen(source)
                self.add_message("AI: Samajh raha hoon...")
                command = r.recognize_google(audio, language='en-in')
                self.msg_entry.delete(0, tk.END)
                self.msg_entry.insert(0, command)
                self.send_message()
            except sr.UnknownValueError:
                self.add_message("AI: Maaf kijiye, main theek se sun nahin paya.")
            except sr.RequestError:
                self.add_message("AI: Maaf kijiye, service abhi uplabdh nahin hai.")
            except Exception as e:
                self.add_message(f"AI: Ek error aayi hai: {e}")
            finally:
                self.listen_button.config(state=tk.NORMAL, text="Listen 🎤")


    def send_message(self, event=None):
        user_input = self.msg_entry.get()
        if not user_input:
            return

        self.add_message(f"You: {user_input}")
        self.msg_entry.delete(0, tk.END)

        self.process_command(user_input.lower())

    def process_command(self, command):
        """Processes the user's command and generates a response."""
        
        # --- Fun & Information ---
        if "joke" in command:
            response = pyjokes.get_joke()

        elif "weather in" in command:
            city = command.replace("weather in", "").strip()
            if city:
                try:
                    url = f"https://wttr.in/{city}?format=%C+%t"
                    weather_data = requests.get(url)
                    response = f"{city} ka mausam: {weather_data.text}"
                except:
                    response = "Maaf kijiye, main mausam ki jaankari nahin le paya."
            else:
                response = "Kripya shahar ka naam batayein."
        
        elif "what is" in command or "tell me about" in command:
            topic = command.replace("what is", "").replace("tell me about", "").strip()
            if topic:
                page = self.wiki_wiki.page(topic)
                if page.exists():
                    response = f"Wikipedia ke anusaar '{topic}':\n{page.summary[:400]}..."
                else:
                    response = f"Maaf kijiye, mujhe Wikipedia par '{topic}' ke baare mein kuch nahin mila."
            else:
                response = "Kya janna chahte hain, kripya batayein."

        # --- System Commands (Offline) ---
        elif "open notepad" in command:
            response = "Theek hai, Notepad khol raha hoon."; os.system("notepad")
        elif "open calculator" in command:
            response = "Theek hai, Calculator khol raha hoon."; os.system("calc")
        elif "open paint" in command:
            response = "Theek hai, MS Paint khol raha hoon."; os.system("mspaint")
        elif "open command prompt" in command or "open cmd" in command:
            response = "Theek hai, Command Prompt khol raha hoon."; os.system("start cmd")
        elif "open file explorer" in command:
            response = "Theek hai, File Explorer khol raha hoon."; os.system("explorer")
        
        elif "shutdown computer" in command:
            if messagebox.askyesno("Confirm Shutdown", "Kya aap sach mein computer band karna chahte hain?"):
                os.system("shutdown /s /t 1"); response = "Computer band ho raha hai."
            else:
                response = "Shutdown cancel kar diya gaya hai."

        elif "restart computer" in command:
            if messagebox.askyesno("Confirm Restart", "Kya aap sach mein computer restart karna chahte hain?"):
                os.system("shutdown /r /t 1"); response = "Computer restart ho raha hai."
            else:
                response = "Restart cancel kar diya gaya hai."

        elif "time" in command:
            now = datetime.now().strftime("%H:%M:%S"); response = f"Abhi samay hai: {now}"
        elif "hello" in command or "hi" in command:
            response = "Hello! Main aapki kaise madad kar sakta hoon?"

        # --- Online Commands ---
        elif "open youtube" in command:
            response = "Theek hai, YouTube khol raha hoon."; webbrowser.open("https://www.youtube.com")
        elif "open google" in command:
            response = "Theek hai, Google khol raha hoon."; webbrowser.open("https://www.google.com")
        elif "search for" in command:
            query = command.replace("search for", "").strip()
            if query:
                search_url = f"https://www.google.com/search?q={query}"; webbrowser.open(search_url)
                response = f"Theek hai, '{query}' ke liye search kar raha hoon."
            else:
                response = "Kya search karna hai, कृपया batayein."
        
        # --- Default action for anything else ---
        else:
            try:
                search_url = f"https://www.google.com/search?q={command.replace(' ', '+')}"; webbrowser.open(search_url)
                response = f"Mujhe iska seedha jawab nahin pata. Maine aapke liye Google par search kar diya hai."
            except Exception:
                response = "Maaf kijiye, kuch gadbad ho gayi."

        self.add_message(f"AI: {response}")

    def add_message(self, message):
        """Adds a message to the chat display."""
        def update_gui():
            self.chat_area.config(state='normal')
            self.chat_area.insert(tk.END, message + '\n\n')
            self.chat_area.yview(tk.END)
            self.chat_area.config(state='disabled')
        # This ensures GUI updates are done in the main thread
        self.master.after(0, update_gui)

if __name__ == "__main__":
    root = tk.Tk()
    app = AssistantApp(root)
    root.mainloop()

