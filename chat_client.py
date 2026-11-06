
import socket
import threading
import tkinter as tk
from tkinter import messagebox
from datetime import datetime


HOST = "127.0.0.1"
PORT = 5000


class ChatClient:

    def __init__(self, root):

        self.root = root
        self.root.title("Oasis Chat Application")
        self.root.geometry("600x550")
        self.root.configure(bg="#EAF4FF")

        self.client = None
        self.connected = False

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.close_chat
        )

        # Title
        tk.Label(
            root,
            text="Oasis Chat Application",
            font=("Arial", 22, "bold"),
            bg="#EAF4FF",
            fg="#1E3A8A"
        ).pack(pady=15)

        # Chat messages
        self.chat_area = tk.Text(
            root,
            font=("Arial", 11),
            bg="white",
            state="disabled",
            wrap="word"
        )

        self.chat_area.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        # Message input
        input_frame = tk.Frame(
            root,
            bg="#EAF4FF"
        )

        input_frame.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.message_entry = tk.Entry(
            input_frame,
            font=("Arial", 12)
        )

        self.message_entry.pack(
            side="left",
            fill="x",
            expand=True,
            ipady=6
        )

        self.message_entry.bind(
            "<Return>",
            self.send_message
        )

        # Send button
        tk.Button(
            input_frame,
            text="Send",
            font=("Arial", 11, "bold"),
            bg="#2563EB",
            fg="white",
            command=self.send_message
        ).pack(
            side="right",
            padx=5
        )

        # Connect button
        tk.Button(
            root,
            text="Connect to Chat Server",
            font=("Arial", 11, "bold"),
            bg="#16A34A",
            fg="white",
            command=self.connect_server
        ).pack(pady=5)

        # Disconnect button
        tk.Button(
            root,
            text="Disconnect",
            font=("Arial", 11),
            command=self.disconnect
        ).pack(pady=5)

        tk.Label(
            root,
            text="Oasis Infobyte Python Internship",
            font=("Arial", 9),
            bg="#EAF4FF",
            fg="#64748B"
        ).pack(pady=10)

    def display_message(self, message):

        self.chat_area.config(state="normal")

        self.chat_area.insert(
            tk.END,
            message + "\n"
        )

        self.chat_area.see(tk.END)

        self.chat_area.config(state="disabled")

    def connect_server(self):

        if self.connected:
            messagebox.showinfo(
                "Connected",
                "Already connected to the server."
            )
            return

        try:

            self.client = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            self.client.connect((HOST, PORT))

            self.connected = True

            self.display_message(
                "Connected to chat server."
            )

            threading.Thread(
                target=self.receive_messages,
                daemon=True
            ).start()

        except OSError as e:

            if self.client:
                self.client.close()

            self.client = None

            messagebox.showerror(
                "Connection Error",
                f"Unable to connect.\n{e}"
            )

    def receive_messages(self):

        buffer = ""

        try:

            while self.connected:

                data = self.client.recv(1024)

                if not data:
                    break

                buffer += data.decode("utf-8")

                while "\n" in buffer:

                    message, buffer = buffer.split(
                        "\n", 1
                    )

                    message = message.strip()

                    if message:
                        self.root.after(
                            0,
                            self.display_message,
                            message
                        )

        except OSError:
            pass

        finally:

            if self.connected:

                self.connected = False

                self.root.after(
                    0,
                    self.display_message,
                    "Disconnected from server."
                )

    def send_message(self, event=None):

        if not self.connected:

            messagebox.showwarning(
                "Not Connected",
                "Connect to the server first."
            )

            return

        message = self.message_entry.get().strip()

        if not message:
            return

        if message == "/quit":

            self.disconnect()
            return

        timestamp = datetime.now().strftime(
            "%H:%M:%S"
        )

        self.display_message(
            f"[{timestamp}] You: {message}"
        )

        try:

            self.client.sendall(
                (message + "\n").encode("utf-8")
            )

            self.message_entry.delete(
                0,
                tk.END
            )

        except OSError:

            messagebox.showerror(
                "Error",
                "Unable to send message."
            )

            self.disconnect()

    def disconnect(self):

        if not self.connected:
            return

        self.connected = False

        try:

            self.client.sendall(
                "/quit\n".encode("utf-8")
            )

        except OSError:
            pass

        try:
            self.client.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass

        try:
            self.client.close()
        except OSError:
            pass

        self.client = None

        self.display_message(
            "You disconnected."
        )

    def close_chat(self):

        self.disconnect()

        self.root.destroy()


if __name__ == "__main__":

    root = tk.Tk()

    app = ChatClient(root)

    root.mainloop()
