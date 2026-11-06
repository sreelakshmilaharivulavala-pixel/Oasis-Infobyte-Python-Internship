
import tkinter as tk
from tkinter import messagebox
import requests


class WeatherApp:

    def __init__(self, root):

        self.root = root
        self.root.title("Weather Application")
        self.root.geometry("500x520")
        self.root.resizable(False, False)
        self.root.configure(bg="#EAF4FF")

        tk.Label(
            root,
            text="Weather Application",
            font=("Arial", 24, "bold"),
            bg="#EAF4FF",
            fg="#1E3A8A"
        ).pack(pady=25)

        tk.Label(
            root,
            text="Enter your city name",
            font=("Arial", 12),
            bg="#EAF4FF"
        ).pack()

        self.city_entry = tk.Entry(
            root,
            font=("Arial", 14),
            justify="center"
        )
        self.city_entry.pack(pady=15, ipadx=30, ipady=5)

        tk.Button(
            root,
            text="Get Weather",
            font=("Arial", 12, "bold"),
            bg="#2563EB",
            fg="white",
            command=self.get_weather
        ).pack(pady=10)

        self.result_label = tk.Label(
            root,
            text="Weather information will appear here",
            font=("Arial", 12),
            bg="#EAF4FF",
            justify="center"
        )
        self.result_label.pack(pady=30)

        tk.Label(
            root,
            text="Oasis Infobyte Python Internship",
            font=("Arial", 9),
            bg="#EAF4FF",
            fg="#64748B"
        ).pack(side="bottom", pady=15)

    def get_weather(self):

        city = self.city_entry.get().strip()

        if not city:
            messagebox.showerror(
                "Error",
                "Please enter a city name."
            )
            return

        # Replace with your own OpenWeatherMap API key
        api_key = "123456789"

        if api_key == "YOUR_API_KEY":
            messagebox.showwarning(
                "API Key Required",
                "Please add your OpenWeatherMap API key."
            )
            return

        url = (
            "https://api.openweathermap.org/data/2.5/weather"
            f"?q={city}&appid={api_key}&units=metric"
        )

        try:

            response = requests.get(url, timeout=10)

            if response.status_code == 404:
                messagebox.showerror(
                    "City Not Found",
                    "Please enter a valid city name."
                )
                return

            response.raise_for_status()

            data = response.json()

            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind = data["wind"]["speed"]
            condition = data["weather"][0]["description"]

            result = (
                f"City: {data['name']}\n\n"
                f"Temperature: {temperature} °C\n"
                f"Condition: {condition.title()}\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind} m/s"
            )

            self.result_label.config(
                text=result,
                fg="#1E3A8A"
            )

        except requests.exceptions.Timeout:
            messagebox.showerror(
                "Timeout",
                "Weather request timed out. Try again."
            )

        except requests.exceptions.ConnectionError:
            messagebox.showerror(
                "Connection Error",
                "Please check your internet connection."
            )

        except requests.exceptions.RequestException as e:
            messagebox.showerror(
        "Weather API Error",
        f"Error details:\n{e}"
    )

        except (KeyError, ValueError):
            messagebox.showerror(
                "Error",
                "Invalid weather data received."
            )


if __name__ == "__main__":

    root = tk.Tk()

    app = WeatherApp(root)

    root.mainloop()
