"""
    See README.md
"""

# External modules
from tkinter  import *               # GUI framework
from time     import strftime        # needed for time widget
import time
import threading

# Own modules
from Weather_API    import Weather_API       # Data class to fetch and store weather data
from Forecast_Frame import Forecast_Frame # GUI class to enter search query and show weather information from Weather_API
from Help_Frame     import Help_Frame         # GUI class to show help information
from API_Key_Frame  import API_Key_Frame   # GUI class to enter API Key for Weather_API

##################
# MAIN APP CLASS
##################
class App_Window( Tk ):
    logo = None

    # Create Weather data store
    weather_api = Weather_API(
        url = 'http://api.weatherapi.com/v1/forecast.json' ,
        API_key_file = 'weatherapi.key'
    )

    # App constructor
    def __init__( self , title:str , geometry:str ):
        super().__init__()
        
        # Set up app window
        self.geometry( geometry )
        self.title( title )

        # Make the app always on top
        self.wm_attributes( '-topmost' , True )

        self.columnconfigure( 0 , weight=1 )
        self.logo = PhotoImage( file='logo.png' ) 

    # Create App GUI with the folowing layout: 
    #   * header to display time and logo - diasplaied at all times
    #   * main frame to display navigable frames:
    #      - forecast frame to allow search and display of weather information
    #      - help frame to display help information
    #      - API Key grame to set/update an API Key 
    def create_GUI( self ):
        # Create window layout
        header_frame = Frame( self )
        header_frame.grid( row=0 , column=0 )

        main_frame = Frame( self )
        main_frame.grid( row=1 , column=0 )

        # Create header frame content and display it
        Label( header_frame , image=self.logo ).grid( row=0 , column=0 )
        
        time_label = Label( header_frame , font=( 'Arial' , 20 ) , fg='#FF781F' )
        time_label.grid( row=0 , column=1 )
        def show_time( label:object ):              # recursive endless loop to update the clock
            label.config( text = '   ' + strftime( '%H:%M:%S' ) )
            label.after( 1000 , show_time , label ) # recursive call every 1000ms
        show_time( time_label )                     # start lable update loop

        # Create 3 navigable frames with links to Weather API
        forecast_nav_frame = Forecast_Frame( main_frame , 
            data_apis={ 'Weather API': self.weather_api } 
        )
        help_nav_frame     = Help_Frame(    main_frame )
        api_key_nav_frame  = API_Key_Frame( main_frame, 
            data_apis={ 'Weather API': self.weather_api } 
        )
        # Stack all frames in the same grid location
        forecast_nav_frame.grid( row=0 , column=0 )
        help_nav_frame.grid( row=0 , column=0 )
        api_key_nav_frame.grid( row=0 , column=0 )

        # Set navigation
        forecast_nav_frame.set_nav_frames( {
            'Help': help_nav_frame
        })
        help_nav_frame.set_nav_frames( {
            "Get Weather": forecast_nav_frame,
            "API Key":     api_key_nav_frame
        })
        api_key_nav_frame.set_nav_frames({
            "Get Weather": forecast_nav_frame,
            "Help":        help_nav_frame
        })

        # Create all widgets
        forecast_nav_frame.widgets()
        help_nav_frame.widgets()
        api_key_nav_frame.widgets()

        # Navigate depending on existance of an API Key
        if self.weather_api.has_API_Key():
            forecast_nav_frame.render() # query the API for weather information
        else:
            api_key_nav_frame.render()  # show dialog to set API Key
        
        # Start auto refresh daemon
        def auto_refresh( forecast_nav_frame:object ):
            while True:
                time.sleep( 12*3600 ) # Refresh every 12h
                forecast_nav_frame.get_forecast( forecast_nav_frame.get_query() )

        thr = threading.Thread( target = auto_refresh , args=( forecast_nav_frame, ) , daemon=True ) 
        thr.start()

##################
# MAIN APP RUN
##################

if __name__ == "__main__":
    app = App_Window( title='Duckling Weather App' , geometry='500x600' ) # Configure the app
    app.create_GUI()  # Create all components
    app.mainloop()    # Display the app window
