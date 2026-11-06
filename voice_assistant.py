
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import pyttsx3
import webbrowser
from datetime import datetime
import threading


class VoiceAssistant:

    def __init__(self, root):

        self.root = root

        self.root.title("Oasis Voice Assistant")
        self.root.geometry("550x500")
        self.root.configure(bg="#EAF4FF")
        self.root.resizable(False, False)

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", 160)

        self.recognizer = sr.Recognizer()

        # Title
        tk.Label(
            root,
            text="Voice Assistant",
            font=("Arial", 24, "bold"),
            bg="#EAF4FF",
            fg="#1E3A8A"
        ).pack(pady=20)

        tk.Label(
            root,
            text="Your personal Python assistant",
            font=("Arial", 11),
            bg="#EAF4FF",
            fg="#64748B"
        ).pack()

        # Status
        self.status_label = tk.Label(
            root,
            text="Click Start Listening",
            font=("Arial", 12),
            bg="#EAF4FF"
        )

        self.status_label.pack(pady=20)

        # Output
        self.output = tk.Text(
            root,
            height=10,
            width=55,
            font=("Arial", 11),
            state="disabled",
            wrap="word"
        )

        self.output.pack(padx=20, pady=10)

        # Start button
        tk.Button(
            root,
            text="Start Listening",
            font=("Arial", 12, "bold"),
            bg="#2563EB",
            fg="white",
            command=self.start_listening
        ).pack(pady=10)

        # Exit button
        tk.Button(
            root,
            text="Exit",
            font=("Arial", 11),
            command=self.root.destroy
        ).pack(pady=5)

        tk.Label(
            root,
            text="Oasis Infobyte Python Internship",
            font=("Arial", 9),
            bg="#EAF4FF",
            fg="#64748B"
        ).pack(side="bottom", pady=10)

    def speak(self, text):

        self.engine.say(text)
        self.engine.runAndWait()

    def display(self, text):

        self.output.config(state="normal")

        self.output.insert(
            tk.END,
            text + "\n"
        )

        self.output.see(tk.END)

        self.output.config(state="disabled")

    def start_listening(self):

        threading.Thread(
            target=self.listen,
            daemon=True
        ).start()

    def listen(self):

        try:

            self.root.after(
                0,
                self.status_label.config,
                {"text": "Listening..."}
            )

            with sr.Microphone() as source:

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=8
                )

            command = self.recognizer.recognize_google(
                audio
            )

            command = command.lower()

            self.root.after(
                0,
                self.display,
                "You: " + command
            )

            self.process_command(command)

        except sr.WaitTimeoutError:

            self.root.after(
                0,
                self.display,
                "No speech detected."
            )

        except sr.UnknownValueError:

            self.root.after(
                0,
                self.display,
                "Sorry, I could not understand."
            )

            self.speak(
                "Sorry, I could not understand."
            )

        except sr.RequestError:

            self.root.after(
                0,
                self.display,
                "Speech recognition service unavailable."
            )

            self.speak(
                "Speech recognition service is unavailable."
            )

        except OSError:

            self.root.after(
                0,
                self.display,
                "Microphone not available."
            )

            self.speak(
                "Microphone not available."
            )

        finally:

            self.root.after(
                0,
                self.status_label.config,
                {"text": "Click Start Listening"}
            )

    def process_command(self, command):

        response = ""

        if "hello" in command:

            response = "Hello! How can I help you?"

        elif "time" in command:

            current_time = datetime.now().strftime(
                "%I:%M %p"
            )

            response = (
                "The current time is "
                + current_time
            )

        elif "date" in command:

            current_date = datetime.now().strftime(
                "%d %B %Y"
            )

            response = (
                "Today's date is "
                + current_date
            )

        elif "open google" in command:

            webbrowser.open(
                "https://www.google.com"
            )

            response = "Opening Google."

        elif "open youtube" in command:

            webbrowser.open(
                "https://www.youtube.com"
            )

            response = "Opening YouTube."

        elif "search" in command:

            query = command.replace(
                "search",
                "",
                1
            ).strip()

            if query:

                webbrowser.open(
                    "https://www.google.com/search?q="
                    + query.replace(" ", "+")
                )

                response = (
                    "Searching for "
                    + query
                )

            else:

                response = "Please say what you want to search."

        elif "exit" in command or "stop assistant" in command:

            response = "Goodbye!"

            self.display(
                "Assistant: " + response
            )

            self.speak(response)

            self.root.after(
                0,
                self.root.destroy
            )

            return

        else:

            response = (
                "Sorry, I don't know that command."
            )

        self.root.after(
            0,
            self.display,
            "Assistant: " + response
        )

        self.speak(response)


if __name__ == "__main__":

    root = tk.Tk()

    app = VoiceAssistant(root)

    root.mainloop()
