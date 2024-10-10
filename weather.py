import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import geocoder
import io
from datetime import datetime

API_KEY = '70bcf74ca6138e62bfcfe00ce7d6e89e'
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'
FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast?'

def get_weather_data(city, unit):
    try:
        complete_url = BASE_URL + "appid=" + API_KEY + "&q=" + city + "&units=" + unit
        response = requests.get(complete_url)
        data = response.json()

        if data['cod'] == 200:
            return data
        else:
            messagebox.showerror("Error", f"City '{city}' not found!")
            return None
    except Exception as e:
        messagebox.showerror("Error", "Failed to retrieve data!")
        return None

def get_forecast_data(city, unit):
    try:
        complete_url = FORECAST_URL + "appid=" + API_KEY + "&q=" + city + "&units=" + unit
        response = requests.get(complete_url)
        data = response.json()

        if data['cod'] == '200':
            return data
        else:
            messagebox.showerror("Error", f"City '{city}' not found!")
            return None
    except Exception as e:
        messagebox.showerror("Error", "Failed to retrieve data!")
        return None

def show_weather():
    city = city_entry.get()
    unit = 'metric' if var_unit.get() == 'Celsius' else 'imperial'

    if city:
        weather_data = get_weather_data(city, unit)
        if weather_data:
            city_name = weather_data['name']
            temp = weather_data['main']['temp']
            wind_speed = weather_data['wind']['speed']
            description = weather_data['weather'][0]['description']
            icon_id = weather_data['weather'][0]['icon']

            weather_label.config(text=f"Weather in {city_name}: {description.capitalize()}")
            temp_label.config(text=f"Temperature: {temp}°{var_unit.get()}")
            wind_label.config(text=f"Wind Speed: {wind_speed} m/s")

            # Display weather icon
            icon_url = f"http://openweathermap.org/img/wn/{icon_id}@2x.png"
            img_data = requests.get(icon_url).content
            img = Image.open(io.BytesIO(img_data))
            img = img.resize((100, 100))
            weather_icon = ImageTk.PhotoImage(img)
            icon_label.config(image=weather_icon)
            icon_label.image = weather_icon
    else:
        messagebox.showwarning("Input Error", "Please enter a city name!")

def get_current_location():
    try:
        g = geocoder.ip('me')
        if g.ok:
            return g.city
        else:
            messagebox.showerror("Location Error", "Could not detect location automatically")
            return None
    except Exception as e:
        messagebox.showerror("Location Error", "Could not detect location automatically")
        return None

def auto_detect_location():
    city = get_current_location()
    if city:
        city_entry.delete(0, tk.END)
        city_entry.insert(0, city)
        show_weather()

def show_forecast():
    city = city_entry.get()
    unit = 'metric' if var_unit.get() == 'Celsius' else 'imperial'
    if city:
        forecast_data = get_forecast_data(city, unit)
        if forecast_data:
            forecast_text = ""
            for item in forecast_data['list'][:8]:
                time = datetime.utcfromtimestamp(item['dt']).strftime('%Y-%m-%d %H:%M:%S')
                temp = item['main']['temp']
                description = item['weather'][0]['description']
                forecast_text += f"Time: {time}, Temp: {temp}°{var_unit.get()}, {description.capitalize()}\n"
            forecast_label.config(text=forecast_text)
    else:
        messagebox.showwarning("Input Error", "Please enter a city name!")

app = tk.Tk()
app.title("Weather App")
app.geometry("400x600")

city_label = tk.Label(app, text="Enter City")
city_label.pack(pady=10)
city_entry = tk.Entry(app, width=30)
city_entry.pack()

var_unit = tk.StringVar(value='Celsius')
celsius_rb = tk.Radiobutton(app, text="Celsius", variable=var_unit, value='Celsius')
fahrenheit_rb = tk.Radiobutton(app, text="Fahrenheit", variable=var_unit, value='Fahrenheit')
celsius_rb.pack()
fahrenheit_rb.pack()

detect_location_button = tk.Button(app, text="Detect Location", command=auto_detect_location)
detect_location_button.pack(pady=10)
get_weather_button = tk.Button(app, text="Get Weather", command=show_weather)
get_weather_button.pack(pady=10)

weather_label = tk.Label(app, text="Weather Info Will Appear Here")
weather_label.pack(pady=10)
temp_label = tk.Label(app, text="")
temp_label.pack(pady=10)
wind_label = tk.Label(app, text="")
wind_label.pack(pady=10)
icon_label = tk.Label(app, text="")
icon_label.pack(pady=10)

forecast_button = tk.Button(app, text="Get Hourly Forecast", command=show_forecast)
forecast_button.pack(pady=10)
forecast_label = tk.Label(app, text="Hourly Forecast Will Appear Here", wraplength=300, justify='left')
forecast_label.pack(pady=10)

app.mainloop()
