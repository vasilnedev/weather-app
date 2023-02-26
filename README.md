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
<ul>
<li>**app.00.py** - Concept design - a single file, fully functional application without classes and error handling</li>
<li>**app.01.py** - Main Application foundation class and Basic Frame class</li>
<li>**app.02.py** - Added all visual classes (inhereting Basic Frame), but no data class</li>
<li>**app.03.py** - Added data (API) class, without image supprot</li>
<li>**...**</li>
<li>**app.py**    - final application with split class files, error handling and detailed comments</li>
<li>**Weather_API.py** - class to fetch and store all data from the weather API</li>
<li>**Basic_Frame.py** - a basic frame that clears it's container and render new widgets - to be inherited by all GUI frames</li>
<li>**Forecast_Frame.py** - main view with query dialog and view of the forcast data</li>
<li>**API_Key_Frame.py** - API Key dialog</li>
<li>**Help_Frame.py** - Help information</li>
</ul>

### Experiments
**basic-gui.py** - experiment with tkinter GUI
**basic-gui-threads.py** - use Threading to avid bloking the app in case of slow operations e.g. API calls
