from tkinter import *
from tkinter import ttk
from time    import strftime

import requests

# Get WeatherAPI Key from secure location (excluded from Git)
f = open("weatherapi.key", "r")
WeatherAPI_key = f.read()
f.close()

# Retrive data from API
def get_forecast( query:str , label:object ):  
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': WeatherAPI_key, 
        'q': query,
        'aqi': 'no'
    }
    res = requests.get( url , params=params )
    if res.status_code == 200: # HTTP status code 200 - OK
        data = res.json()
        label.config( text=data['current']['temp_c'] )    
    else:
        print( "Ooops :(" )
        print( res.reason )


# GUI form
def gui_form( parent:object ):

    # Help function to update every second a time label
    def my_time( label:object ):
        label.config( text= strftime( '%H:%M:%S %p | %x' ) )
        label.after( 1000 , my_time , label ) # recursive call every 1000ms

    # Initilise Frame for all widgets
    frm = ttk.Frame( parent , padding=5 )
    frm.grid()
    
    # Row 1 - title
    ttk.Label(  frm, text="Weather App").grid( row=0 , column=0 , columnspan=2 )

    # Row 2 - current time and date
    time_label = ttk.Label( frm )
    time_label.grid( row=1 , column=0 , columnspan=2 )
    my_time( time_label ) # start lable update loop

    # Row 3 - Query
    ttk.Label( frm, text="Query:" ).grid( row=2 , column=0 )
    query_entry = ttk.Entry( frm , width=10 )
    query_entry.grid( row=2 , column=1 )
    
    # Row 4 - Buttons
    ttk.Button( frm, text="Get Forecast", command = lambda: get_forecast( query_entry.get() , temp_c_label ) ).grid( row=3 , column=0 )
    ttk.Button( frm, text="Quit", command=parent.destroy ).grid( row=3 , column=1 )

    # Row 5 - Current conditions
    ttk.Label(  frm, text="Temp. C").grid( row=4 , column=0 )
    temp_c_label = ttk.Label( frm )
    temp_c_label.grid( row=4 , column=1 )

##################
# MAIN APP
##################
root = Tk(  )

gui_form( root )

root.mainloop()
