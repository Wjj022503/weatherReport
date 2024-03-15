 from cProfile import label
from logging import config
from tkinter import * # building GUI
import tkinter as tk
import geopy.geocoders
from geopy.geocoders import Nominatim # convert addresses into geographic coordinates
from tkinter import ttk, messagebox
from timezonefinder import TimezoneFinder # finding the time zone of a location based on its latitude and longtitude
from datetime import datetime # work with dates and times
import requests # make HTTP requests to web servers
import pytz # provices time zone calculations with respect to daylight saving time
import certifi
import ssl
import sys
import os

#get resource path for .exe
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

# main window
root = Tk()
root.title("Weather App")
root.iconbitmap(resource_path("weatherImage\icon_program.ico"))
root.geometry("1000x600+250+100")
root.resizable(False,False)
root.configure(bg="lightblue")

#find newest SSL certificate
ctx = ssl.create_default_context(cafile=certifi.where())
geopy.geocoders.options.default_ssl_context = ctx

#get location, time and weather by API
def get_weather():
    try:
        city = textfield.get()
        geoLocator = Nominatim(user_agent="getLocation")
        location = geoLocator.geocode(city)
        obj = TimezoneFinder()
        result = obj.timezone_at(lng=location.longitude,lat=location.latitude)
        
        home = pytz.timezone(result)
        localTime = datetime.now(home)
        currentTime = localTime.strftime("%I:%M %p")
        clock.config(text=currentTime)
        weatherL.config(text="Current Weather")

        # weather
        apiKey = "0cd6299a00a1b86aa3b2ebf761c245c0"
        api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + apiKey
        jsonData = requests.get(api).json()
        cond = jsonData['weather'][0]['main']
        description = jsonData['weather'][0]['description']
        temp = int(jsonData['main']['temp']-273.15)
        pressure = jsonData['main']['pressure']
        humidity = jsonData['main']['humidity']
        wind = jsonData['wind']['speed']
        temparatureL.config(text=(temp,"°"))
        conditionL.config(text=(cond,"|","Feels","Like",temp,"°"))
        show_weather_logo(cond,localTime)

        windL.config(text=wind)
        humidL.config(text=humidity)
        desL.config(text=description)
        prsL.config(text=pressure)
    except Exception as e:
        messagebox.showerror("Weather App", "Invalid Entry, please enter correct country/city name.")

#search box
SearchBar = PhotoImage(file=resource_path("weatherImage/search_bar.png"))
mySearchBar = Label(image=SearchBar,bg="lightblue")
mySearchBar.place(x = 20, y = 20)

#search box textfield
textfield = tk.Entry(root, justify="center",width=17,font=("poppins",25,"bold"),bg="#323b3e", border=0, fg="white")
textfield.place(x=50,y=40)
textfield.focus()

#search button
SearchButton = PhotoImage(file= resource_path("weatherImage/search.png"))
mySearchButton = Button(image=SearchButton, borderwidth=0,cursor="hand2",bg="#323b3e",command=get_weather)
mySearchButton.place(x=400,y=34)

#weather logo
weatherImage = PhotoImage(file=resource_path("weatherImage/normal.png"))
myWeatherImg = Label(image=weatherImage,bg="lightblue")
myWeatherImg.place(x=160,y=180)

#change weather logo
def update_weather_image(newImagePath):
    global myWeatherImg
    newWeatherImg = PhotoImage(file=resource_path(newImagePath))
    myWeatherImg.configure(image=newWeatherImg)
    myWeatherImg.image = newWeatherImg

#identify weather logo to show
def show_weather_logo(cond,time):
    match cond:
        case "Clouds":
            if(6 <= time.hour <= 18):
                return update_weather_image("weatherImage/cloudy.png")
            else:
                return update_weather_image("weatherImage/cloudy_night.png")
        case "Thunderstorm":
            if(6 <= time.hour <= 18):
                return update_weather_image("weatherImage/thunderstorm.png")
            else:
                return update_weather_image("weatherImage/thunderstorm_night.png")
        case "Drizzle" | "Rain":
            return update_weather_image("weatherImage/rain.png")
        case "Snow":
            return update_weather_image("weatherImage/snow.png")
        case "Clear":
            return update_weather_image("weatherImage/sunny.png")
        case "Squall","Tornado":
            return update_weather_image("weatherImage/wind.png")
        case "Mist" | "Smoke" | "Haze" | "Dust" | "Fog" | "Sand" | "Dust" | "Ash":
            return update_weather_image("weatherImage/haze.png")
        case _:
            return

#weather informations frame
frameImg = PhotoImage(file=resource_path("weatherImage/box.png"))
myFrameImg = Label(image=frameImg,bg="lightblue")
myFrameImg.pack(padx=5,pady=5,side=BOTTOM)

#time label
weatherL = Label(root, font=("arial",15,"bold"),bg="lightblue")
weatherL.place(x=40, y=110)
clock = Label(root, font=("Helvetica",20),bg="lightblue")
clock.place(x=40, y=140)

#weather informations label
windLabel = Label(root,text="Wind",font=("Helvetica",15,'bold'),fg="white",bg="#1ab5ef")
windLabel.place(x=180,y=500)

humidLabel = Label(root,text="Humidity",font=("Helvetica",15,'bold'),fg="white",bg="#1ab5ef")
humidLabel.place(x=300,y=500)

desLabel = Label(root,text="Description",font=("Helvetica",15,'bold'),fg="white",bg="#1ab5ef")
desLabel.place(x=440,y=500)

prsLabel = Label(root,text="Pressure",font=("Helvetica",15,'bold'),fg="white",bg="#1ab5ef")
prsLabel.place(x=720,y=500)

temparatureL=Label(font=("arial",90,"bold"),fg="#ee666d",bg="lightblue")
temparatureL.place(x=580,y=150)

conditionL=Label(font=("arial",20,"bold"),fg="#ee666d",bg="lightblue")
conditionL.place(x=580,y=280)

windL=Label(text="...",font=("arial",20,"bold"),bg="#1ab5ef")
windL.place(x=180,y=530)

humidL=Label(text="...",font=("arial",20,"bold"),bg="#1ab5ef")
humidL.place(x=300,y=530)

desL=Label(text="...",font=("arial",20,"bold"),bg="#1ab5ef")
desL.place(x=440,y=530)

prsL=Label(text="...",font=("arial",20,"bold"),bg="#1ab5ef")
prsL.place(x=720,y=530)

#main event loop
root.mainloop()

