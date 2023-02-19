# weather-app

The goal of this project is to create a weather app in Python that shows the current weather conditions and forecast for a specific location.

Here are the steps taken to create this project:
* Use the requests library to make an API call to a weather service (e.g. OpenWeatherMap) to retrieve the weather data for a specific location.
* Use the json library to parse the JSON data returned by the API call.
* Use the tkinter library to create a GUI for the app, including widgets such as labels, buttons and text boxes.
* Use the Pillow library to display the weather icons.
* Use the datetime library to display the current time and date.

Completed tasks:
* Create 3 forms: main form for forecast, API Key entry form and Help form
* Use www.weatherapi.com API for getting current conditiopns and forecast
* Use icons from www.weatherapi.com API
* Display current date and time

To do:
* Allow changing the API Key from the app
* Make robust error handling

Notes:
1. When starting for fist time, the app will require API Key from www.weatherapi.com 
2. To reset the API Key, exit the app, delete the weatherapi.key file and start the app again
