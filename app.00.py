from tkinter import *
from tkinter import ttk
from time    import strftime
from PIL     import Image , ImageTk
from io      import BytesIO
import requests

##########################
# Global Variables
##########################
API_key_file   = 'weatherapi.key'
weatherAPI_key = None # Variable to store the API Key
imageTk_icon   = None # Variable for ImageTk icon

##########################
# Common functions
##########################

# Clear root GUI window
def clear_root( root:object ):
    for frame in root.winfo_children():
        frame.destroy()

##########################
# Help form
##########################

def close_help_form( root:object ):
    clear_root( root )    # Clear the root window
    forecast_form( root ) # Show the forecast form

# Help form will be called by a help button to show query examples
def help_form( root:object ):
    clear_root( root )
    global imageTk_icon
    instructions = '''

For detailed documentation visit:

            www.weatherapi.com

For quick reference, see these query examples:
Latitude and Longitude (Decimal degree) e.g: 48.8567,2.3508
city name e.g.: Paris
US zip e.g.: 10001
UK postcode e.g: SW1
Canada postal code e.g: G2J
metar:<metar code> e.g: metar:EGLL
iata:<3 digit airport code> e.g: iata:DXB
auto:ip IP lookup e.g: auto:ip
IP address (IPv4 and IPv6 supported) e.g: 100.0.0.1

'''
    frm = ttk.Frame( root , padding=5 )
    frm.grid()
    # Row 1 - Logo
    image_icon   = Image.open( 'logo.png' )
    imageTk_icon = ImageTk.PhotoImage( image_icon )
    ttk.Label( frm , image=imageTk_icon ).grid( row=0 , column=0 )
    # Row 2 - Instructions
    ttk.Label( frm , text=instructions ).grid( row=1 , column=0 )
    # Row 3 - Close Button
    ttk.Button( frm, text="Close", 
        command = lambda: 
            close_help_form( root ) 
    ).grid( row=2 , column=0 )

########################################
# Weather forecast form (main form)
########################################

# Retrive data from API and update form widgets
def fetch_forecast( query:str , form:object ):
    global weatherAPI_key 
    global imageTk_icon
    # Send API request like:
    # http://api.weatherapi.com/v1/current.json?key=< API KEY >&q=London&aqi=no
    # For full documentation visit https://www.weatherapi.com site
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        'key': weatherAPI_key, 
        'q': query,
        'aqi': 'no'   # To get air quality data or not
    }
    res = requests.get( url , params=params )  
    # Update widgets
    if res.status_code == 200: # HTTP status code 200 - OK
        # Parse the response to a variable
        data = res.json()
        condition_text = 'The weather condition at {0} is: {1}'.format( 
            data['location'][ 'name' ], 
            data['current'][ 'condition' ][ 'text' ]
        )
        form.nametowidget( 'condition_text' ).config( text=condition_text )
        
        res = requests.get( 'http:' + str( data['current'][ 'condition' ][ 'icon' ] ) )
        if res.status_code == 200:
            image_icon   = Image.open( BytesIO( res.content ) )
            imageTk_icon = ImageTk.PhotoImage( image_icon )
            form.nametowidget( 'condition_icon' ).config( image=imageTk_icon )
        else:
            print( res.reason )

        form.nametowidget( 'temp_c' ).config( text='{} °C'.format( str( data['current'][ 'temp_c' ] ) ) )
        form.nametowidget( 'temp_f' ).config( text='{} °F'.format( str( data['current'][ 'temp_f' ] ) ) )
    else:
        form.nametowidget( 'condition_text' ).config( text='Ooops, something went wrong. The API response is:\n{}'.format( res.reason ) )

# Main forecast form
def forecast_form( root:object ):
    global imageTk_icon
    # Initilise Frame for all widgets
    frm = ttk.Frame( root , padding=5)
    frm.grid()

    # Row 1 - title
    ttk.Label( frm , text="Local time" ).grid( row=0 , column=0 )
    # Local Time label
    def my_time( label:object ): # Help function to update the time label every second
        label.config( text= strftime( '%H:%M:%S %p | %x' ) )
        label.after( 1000 , my_time , label ) # recursive call every 1000ms

    time_label = ttk.Label( frm )
    time_label.grid( row=0 , column=1 )
    my_time( time_label ) # start lable update loop

    # Row 2 - current time and date
    query_entry = ttk.Entry( frm )
    query_entry.grid( row=1 , column=0 )
    query_entry.focus()
    ttk.Button( frm , text="Get Weather",
        command = lambda: 
            fetch_forecast( query_entry.get() , frm ) 
    ).grid( row=1 , column=1 )
    ttk.Button( frm , text="Help",
        command = lambda: 
            help_form( root ) 
    ).grid( row=1 , column=2 )

    # Row 3 - Current conditions - icon
    image_icon   = Image.open( 'logo.png' )
    imageTk_icon = ImageTk.PhotoImage( image_icon )
    ttk.Label( frm , name = 'condition_icon' , image=imageTk_icon ).grid( row=2 , column=0 , columnspan=3 )

    # Row 4 - Current conditions - text
    ttk.Label( frm,  name = 'condition_text' ).grid( row=3 , column=0 , columnspan=3 )

    # Row 5 - Current conditions - temperatures
    ttk.Label( frm , name = 'temp_c' ).grid( row=4 , column=0 )
    ttk.Label( frm,  name = 'temp_f' ).grid( row=4 , column=1 , columnspan=2 )

##########################
# API Key form
##########################

# Save API key into a file
def save_API_key( key:str , root:object ):
    global API_key_file
    global weatherAPI_key
    weatherAPI_key = key
    try:
        f = open( API_key_file , "w" )
        f.write( key )
        f.close()
    except Exception: pass # For now do nothing if fail to write
    clear_root( root )
    forecast_form( root )

# API Key form to be displaied if there is no API Key file
def api_key_form( root:object ):
    global imageTk_icon
    instructions = '''

This application requires an API Key from 

           www.weartherapi.com

Please visit the site and read the documentation. 

Once you have an API Key, use this form 
to save it and use this application.

'''
    frm = ttk.Frame( root , padding=5 )
    frm.grid()
    # Row 1 - Logo
    image_icon   = Image.open( 'logo.png' )
    imageTk_icon = ImageTk.PhotoImage( image_icon )
    ttk.Label( frm , image=imageTk_icon ).grid( row=0 , column=0 , columnspan=2 )
    # Row 2 - Instructions
    ttk.Label( frm , text=instructions ).grid( row=1 , column=0 , columnspan=2 )
    # Row 3 - Enter Key
    query_entry = ttk.Entry( frm )
    query_entry.grid( row=2 , column=0 )
    query_entry.focus()
    ttk.Button( frm, text="Save API Key", 
        command = lambda: 
            save_API_key( query_entry.get() , root ) 
    ).grid( row=2 , column=1 )

##################
# MAIN APP
##################

root = Tk(  )

try:
    # Get WeatherAPI Key from file
    f = open( API_key_file , "r")
    weatherAPI_key = f.read()
    f.close()
    forecast_form( root ) # Display the forecast form
except FileNotFoundError as e:
    # User entery of API Key
    api_key_form( root )

root.mainloop()
