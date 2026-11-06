
import tkinter as tk
from tkinter import messagebox
import secrets
import string


class PasswordGenerator:

    def __init__(self, root):
        self.root = root

        self.root.title("Password Generator")
        self.root.geometry("500x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#F0F4F8")

        # Title
        title = tk.Label(
            root,
            text="Password Generator",
            font=("Arial", 22, "bold"),
            bg="#F0F4F8",
            fg="#1E293B"
        )
        title.pack(pady=20)

        subtitle = tk.Label(
            root,
            text="Create a strong and secure password",
            font=("Arial", 11),
            bg="#F0F4F8",
            fg="#64748B"
        )
        subtitle.pack()

        # Main frame
        frame = tk.Frame(root, bg="white", padx=25, pady=20)
        frame.pack(padx=25, pady=20, fill="both")

        # Password length
        tk.Label(
            frame,
            text="Password Length",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(anchor="w")

        self.length_entry = tk.Entry(
            frame,
            font=("Arial", 12),
            justify="center"
        )
        self.length_entry.insert(0, "12")
        self.length_entry.pack(fill="x", pady=10)

        # Character options
        self.uppercase = tk.BooleanVar(value=True)
        self.lowercase = tk.BooleanVar(value=True)
        self.digits = tk.BooleanVar(value=True)
        self.symbols = tk.BooleanVar(value=True)

        tk.Checkbutton(
            frame,
            text="Include Uppercase Letters (A-Z)",
            variable=self.uppercase,
            bg="white"
        ).pack(anchor="w")

        tk.Checkbutton(
            frame,
            text="Include Lowercase Letters (a-z)",
            variable=self.lowercase,
            bg="white"
        ).pack(anchor="w")

        tk.Checkbutton(
            frame,
            text="Include Numbers (0-9)",
            variable=self.digits,
            bg="white"
        ).pack(anchor="w")

        tk.Checkbutton(
            frame,
            text="Include Symbols (!@#$)",
            variable=self.symbols,
            bg="white"
        ).pack(anchor="w")

        # Generate button
        tk.Button(
            frame,
            text="Generate Password",
            font=("Arial", 12, "bold"),
            bg="#2563EB",
            fg="white",
            command=self.generate_password
        ).pack(fill="x", pady=15)

        # Password output
        self.password_entry = tk.Entry(
            frame,
            font=("Arial", 13),
            justify="center"
        )
        self.password_entry.pack(fill="x", pady=5)

        # Copy button
        tk.Button(
            frame,
            text="Copy Password",
            command=self.copy_password
        ).pack(fill="x", pady=5)

        # Clear button
        tk.Button(
            frame,
            text="Clear",
            command=self.clear_password
        ).pack(fill="x", pady=5)

        # Footer
        tk.Label(
            root,
            text="Oasis Infobyte Python Internship",
            font=("Arial", 9),
            bg="#F0F4F8",
            fg="#64748B"
        ).pack(pady=5)

    def generate_password(self):

        try:
            length = int(self.length_entry.get())

            if length < 8:
                messagebox.showerror(
                    "Invalid Length",
                    "Password length must be at least 8."
                )
                return

            if length > 128:
                messagebox.showerror(
                    "Invalid Length",
                    "Password length cannot exceed 128."
                )
                return

            character_sets = []

            if self.uppercase.get():
                character_sets.append(string.ascii_uppercase)

            if self.lowercase.get():
                character_sets.append(string.ascii_lowercase)

            if self.digits.get():
                character_sets.append(string.digits)

            if self.symbols.get():
                character_sets.append("!@#$%^&*()-_=+[]{}?")

            if not character_sets:
                messagebox.showerror(
                    "Error",
                    "Select at least one character type."
                )
                return

            if length < len(character_sets):
                messagebox.showerror(
                    "Invalid Length",
                    "Length is too short for selected options."
                )
                return

            # Ensure at least one character from every selected type
            password = [
                secrets.choice(characters)
                for characters in character_sets
            ]

            all_characters = "".join(character_sets)

            # Fill remaining password length
            for _ in range(length - len(password)):
                password.append(
                    secrets.choice(all_characters)
                )

            # Securely shuffle characters
            secrets.SystemRandom().shuffle(password)

            final_password = "".join(password)

            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, final_password)

        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a valid password length."
            )

    def copy_password(self):

        password = self.password_entry.get()

        if not password:
            messagebox.showwarning(
                "Warning",
                "Generate a password first."
            )
            return

        self.root.clipboard_clear()
        self.root.clipboard_append(password)
        self.root.update()

        messagebox.showinfo(
            "Success",
            "Password copied to clipboard!"
        )

    def clear_password(self):

        self.password_entry.delete(0, tk.END)


if __name__ == "__main__":

    root = tk.Tk()

    app = PasswordGenerator(root)

    root.mainloop()
