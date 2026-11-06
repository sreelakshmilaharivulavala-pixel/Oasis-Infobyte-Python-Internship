
import tkinter as tk
from tkinter import messagebox


# ==========================
# BMI CALCULATOR APPLICATION
# ==========================

class BMICalculator:

    def __init__(self, root):

        self.root = root

        self.root.title("BMI Calculator")
        self.root.geometry("450x500")
        self.root.resizable(False, False)

        self.root.configure(bg="#F0F4F8")

        # Title
        title = tk.Label(
            root,
            text="BMI CALCULATOR",
            font=("Arial", 22, "bold"),
            bg="#F0F4F8",
            fg="#1E3A5F"
        )

        title.pack(pady=20)

        # Subtitle
        subtitle = tk.Label(
            root,
            text="Calculate your Body Mass Index",
            font=("Arial", 11),
            bg="#F0F4F8",
            fg="#64748B"
        )

        subtitle.pack(pady=5)

        # Main frame
        self.frame = tk.Frame(
            root,
            bg="white",
            padx=30,
            pady=25
        )

        self.frame.pack(
            padx=25,
            pady=20,
            fill="both"
        )

        # Weight label
        tk.Label(
            self.frame,
            text="Weight (kg)",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(anchor="w")

        # Weight entry
        self.weight_entry = tk.Entry(
            self.frame,
            font=("Arial", 12),
            width=30
        )

        self.weight_entry.pack(
            pady=8,
            fill="x"
        )

        # Height label
        tk.Label(
            self.frame,
            text="Height (meters)",
            font=("Arial", 12, "bold"),
            bg="white"
        ).pack(anchor="w", pady=(15, 0))

        # Height entry
        self.height_entry = tk.Entry(
            self.frame,
            font=("Arial", 12),
            width=30
        )

        self.height_entry.pack(
            pady=8,
            fill="x"
        )

        # Calculate button
        tk.Button(
            self.frame,
            text="Calculate BMI",
            font=("Arial", 12, "bold"),
            bg="#2563EB",
            fg="white",
            activebackground="#1D4ED8",
            command=self.calculate_bmi,
            pady=8
        ).pack(
            pady=20,
            fill="x"
        )

        # Result label
        self.result_label = tk.Label(
            self.frame,
            text="Your BMI will appear here",
            font=("Arial", 13, "bold"),
            bg="white",
            fg="#334155"
        )

        self.result_label.pack(pady=10)

        # Clear button
        tk.Button(
            self.frame,
            text="Clear",
            font=("Arial", 11),
            bg="#E2E8F0",
            fg="#1E293B",
            command=self.clear_fields,
            pady=5
        ).pack(fill="x")

        # Footer
        tk.Label(
            root,
            text="Python Internship Project",
            font=("Arial", 9),
            bg="#F0F4F8",
            fg="#64748B"
        ).pack(pady=5)

    # ==========================
    # Calculate BMI
    # ==========================

    def calculate_bmi(self):

        try:

            weight = float(
                self.weight_entry.get()
            )

            height = float(
                self.height_entry.get()
            )

            # Validate values
            if weight <= 0 or height <= 0:

                messagebox.showerror(
                    "Invalid Input",
                    "Weight and height must be positive numbers."
                )

                return

            # Calculate BMI
            bmi = weight / (height * height)

            # Determine category
            if bmi < 18.5:

                category = "Underweight"
                color = "#2563EB"

            elif bmi < 25:

                category = "Normal"
                color = "#16A34A"

            elif bmi < 30:

                category = "Overweight"
                color = "#EA580C"

            else:

                category = "Obese"
                color = "#DC2626"

            # Display result
            result = (
                f"Your BMI: {bmi:.2f}\n"
                f"Category: {category}"
            )

            self.result_label.config(
                text=result,
                fg=color
            )

        except ValueError:

            messagebox.showerror(
                "Invalid Input",
                "Please enter valid numbers for weight and height."
            )

    # ==========================
    # Clear Fields
    # ==========================

    def clear_fields(self):

        self.weight_entry.delete(0, tk.END)

        self.height_entry.delete(0, tk.END)

        self.result_label.config(
            text="Your BMI will appear here",
            fg="#334155"
        )


# ==========================
# Run Application
# ==========================

if __name__ == "__main__":

    root = tk.Tk()

    app = BMICalculator(root)

    root.mainloop()
