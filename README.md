# weather-app

## Summary
The goal of this project is to create a weather app in Python that shows the current weather conditions and forecast for a specific location.

To create this project, will:
* Use the requests library to make an API call to a weather service (e.g. OpenWeatherMap) to retrieve the weather data for a specific location.
* Use the json library to parse the JSON data returned by the API call.
* Use the tkinter library to create a GUI for the app, including widgets such as labels, buttons and text boxes.
* Use the Pillow library to display the weather icons.
* Use the datetime library to display the current time and date.

Notes:
1. The uses www.weatherapi.com for getting current conditiopns and forecast
2. The app requires an API Key from www.weatherapi.com 
3. The app use icons from www.weatherapi.com as per the API responses

## Development notes
This repository illustrates different development stages and experiments - described in detail in **Stage files** section below.
The final application is (will be) in **app.js** and within multiple class files (file names start with capital letters).

### Stage files:
**app.00.py** - Concept design - a single file, fully functional application without classes and error handling
**app.01.py** - Main Application class and Basic Frame class - foundamental class for all future frames
**app.02.py** - Added all visual classes (inhereting Basic Frame), but no data class
**app.03.py** - Added data (API) class, without image supprot
**...**
**app.py**    - final application with classes, error handling and detailed comments

### Experiments
**basic-gui.py** - experiment with tkinter GUI
**basic-gui-threads.py** - use Threading to avid bloking the app in case of slow operations e.g. API calls
