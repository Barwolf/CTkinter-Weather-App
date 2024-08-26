from customtkinter import *
from CTkMessagebox import CTkMessagebox
from PIL import Image
import datetime
import calendar
import requests
import os
from dotenv import load_dotenv

load_dotenv("../EnvironmentVariables/.env")
API_KEY = os.getenv("weather_app_API_KEY")

today = datetime.datetime.now()
weekday = calendar.day_name[today.weekday()]


def button_event():
    city = city_entry.get()
    state = state_entry.get()
    if city != "":
        response = requests.get(
            f"http://api.openweathermap.org/geo/1.0/direct?q={city},{state},{"US"}&appid={API_KEY}")
        data = response.json()
        lat = data[0]["lat"]
        lon = data[0]["lon"]

        response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=imperial"
                                f"&appid={API_KEY}")
        # print(response.json())
        weather_data = response.json()
        temp = weather_data["main"]["temp"]
        conditions = weather_data["weather"][0]["main"]
        weather_label.configure(text=f"{temp} °F")
        weather_condition.configure(text=f"{conditions}")
        location_label2.configure(text=f"{city_entry.get()}, {state_entry.get()}")
        wind_label.configure(text=f"WIND              {round(weather_data["wind"]["speed"], 2)}")
        humidity_label.configure(text=f"HUMIDITY       {weather_data["main"]["humidity"]}")
        if conditions == "Clouds":
            weather_icon.configure(image=cloud_img)
        elif conditions == "Smoke":
            weather_icon.configure(image=smoke_img)
        else:
            weather_icon.configure(image=sun_img)
    else:
        CTkMessagebox(title="Error", message="Please enter a valid City/State")


# --------- TK setup --------- #

app = CTk()
app.title("Weather")
app.config(padx=100, pady=100)
app.geometry("800x600")
app.resizable(False, False)
set_appearance_mode("dark")

# --------- UI setup --------- #


# --------- Left frame --------- #

frame1 = CTkFrame(master=app, fg_color="#5B7CBB", width=300, height=430, corner_radius=25)
frame1.grid(column=1, row=0)

sun_img = CTkImage(light_image=Image.open("icons/sun.png"), dark_image=Image.open("icons/sun.png"), size=(60, 60))
cloud_img = CTkImage(light_image=Image.open("icons/cloud.png"), dark_image=Image.open("icons/cloud.png"), size=(65, 55))
smoke_img = CTkImage(light_image=Image.open("icons/smoke.png"), dark_image=Image.open("icons/smoke.png"), size=(60, 60))
location_img = CTkImage(light_image=Image.open("icons/location.png"), dark_image=Image.open("icons/location.png"),
                        size=(15, 25))

frame2 = CTkFrame(master=app, fg_color="#212832", width=350, height=400)
frame2.grid(column=2, row=0, columnspan=2)

day_label = CTkLabel(master=frame1, text=f"{weekday}", text_color="#fff", fg_color="transparent",
                     font=("Arial", 25, "bold"))
day_label.place(relx=0.08, rely=0.1)

day_label = CTkLabel(master=frame1, text=f"{today.day}, {today.year}", text_color="#fff", fg_color="transparent",
                     font=("Arial", 15))
day_label.place(relx=0.08, rely=0.18)

location_label1 = CTkLabel(master=frame1, text="", image=location_img, text_color="#fff", fg_color="transparent",
                           font=("Arial", 15))
location_label1.place(relx=0.12, rely=0.3, anchor="e")

location_label2 = CTkLabel(master=frame1, text="######, ##", text_color="#fff", fg_color="transparent",
                           font=("Arial", 15))
location_label2.place(relx=0.14, rely=0.27)


weather_icon = CTkLabel(master=frame1, text="", fg_color="transparent", image=sun_img, font=("", 25))
weather_icon.place(relx=0.08, rely=0.58)

weather_label = CTkLabel(master=frame1, text=f"00 °F", text_color="#fff", fg_color="transparent",
                         font=("Arial", 30, "bold"))
weather_label.place(relx=0.08, rely=0.75)

weather_condition = CTkLabel(master=frame1, text="Sunny", text_color="#fff", fg_color="transparent",
                             font=("Arial", 25, "bold"))
weather_condition.place(relx=0.08, rely=0.85)

# --------- Right Frame --------- #

wind_label = CTkLabel(master=frame2, text=f"WIND               ##", text_color="#fff", fg_color="transparent",
                      font=("Arial", 25, "bold"))
wind_label.place(relx=0.5, rely=0.2, anchor="center")

humidity_label = CTkLabel(master=frame2, text=f"HUMIDITY        ##", text_color="#fff", fg_color="transparent",
                          font=("Arial", 25, "bold"))
humidity_label.place(relx=0.5, rely=0.3, anchor="center")

city_entry = CTkEntry(master=frame2, placeholder_text="City Name", width=200)
city_entry.place(relx=0.5, rely=0.6, anchor="center")

state_entry = CTkEntry(master=frame2, placeholder_text="State Code (Ex: CA)", width=200)
state_entry.place(relx=0.5, rely=0.7, anchor="center")

btn = CTkButton(master=frame2, text="Change Location", command=button_event, width=200, font=("Arial", 15, "bold"),
                height=35, corner_radius=10, hover_color="#343D4B", fg_color="#5B7CBB")
btn.place(relx=0.5, rely=0.8, anchor="center")

app.mainloop()
