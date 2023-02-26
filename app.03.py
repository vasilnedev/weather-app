from tkinter import *
from tkinter import ttk
from time    import strftime
import requests
import threading

class Weather_API():
    API_key_file = 'weatherapi.key'
    url = "http://api.weatherapi.com/v1/current.json"
    API_Key = None
    def __init__( self ):
        self.load_API_Key()

    def load_API_Key( self ):
        try:
            f = open( self.API_key_file , "r" )
            self.API_Key = f.read()
            f.close()
        except Exception: pass

    def save_API_Key( self , key:str ):
        self.API_Key = key
        try:
            f = open( self.API_key_file , "w" )
            f.write( key )
            f.close()
        except Exception: pass # For now do nothing if fail to write

    def has_API_Key( self ):
        return ( self.API_Key is not None )

    def fetch_forecast( self , query:str , callback:object ):
        # Send API request like:
        # http://api.weatherapi.com/v1/current.json?key=< API KEY >&q=London&aqi=no
        # For full documentation visit https://www.weatherapi.com site
        params = {
            'key': self.API_Key, 
              'q': query,
            'aqi': 'no'   # To get air quality data or not
        }
        res = requests.get( self.url , params=params )  
        # Return data
        if res.status_code == 200: # HTTP status code 200 - OK
            callback( True, res.json() )
        else:
            callback( False, res.reason )

class Basic_Frame():
    container = None
    nav_frames = []
    def __init__( self , container:object , nav_frames:list ):
        self.container = container
        self.nav_frames = nav_frames
    
    def set_nav_frame( self , index:int , frame:object ):
        self.nav_frames[ index ] = frame

    def nav_frame( self , index:int ):
        try:
            self.nav_frames[ index ].render()
        except Exception: pass

    def widgets( self , frm:object ): pass # This method shall be rewritten by all child classes

    def render( self ):
        # Check if root is set
        if self.container is not None:
            # clear container
            for child in self.container.winfo_children():
                child.destroy()
            # Create new Frame
            frm = Frame( self.container )
            frm.grid()
            self.widgets( frm )   # Add widgets
            self.container.grid() # Show the container ( frame_main )

class Help_Frame( Basic_Frame ):
    def __init__( self ,  container , nav_frames ):
        super().__init__( container , nav_frames )

    def widgets( self , frm ):
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
        Label(  frm , text=instructions ).grid( row=0 , column=0 , columnspan=2 )
        Button( frm , text="Forecast", command = lambda: self.nav_frame( 0 ) ).grid( row=1 , column=0 )
        Button( frm , text="API Key" , command = lambda: self.nav_frame( 1 ) ).grid( row=1 , column=1 )

class API_Key_Frame( Basic_Frame ):
    def __init__( self ,  container , nav_frames ):
        super().__init__( container , nav_frames )

    def widgets( self , frm ):
        instructions = '''

This application requires an API Key from 

           www.weartherapi.com

Please visit the site and read the documentation. 

Once you have an API Key, use this form 
to save it and use this application.

'''
        Label(  frm , text=instructions ).grid( row=0 , column=0 , columnspan=2 )
        Button( frm , text="Forecast", command = lambda: self.nav_frame( 0 ) ).grid( row=1 , column=0 )
        Button( frm , text="Help"    , command = lambda: self.nav_frame( 1 ) ).grid( row=1 , column=1 )

class Forecast_Frame( Basic_Frame ):
    api = None
    label_condition = None
    label_temp_c = None
    label_temp_f = None

    def __init__( self ,  container , nav_frames , api ):
        super().__init__( container , nav_frames )
        self.api = api

    def widgets( self , frm ):
        query = Entry( frm )
        query.grid( row=0 , column=0 )
        query.focus()
        Button( frm , text="Get Weather",
            command = lambda: self.get_foreecast( query.get() ) 
        ).grid( row=0 , column=1 )
        Button( frm , text="Help" , 
            command = lambda: self.nav_frame( 0 ) 
        ).grid( row=0 , column=2 )
        
        self.label_condition = Label( frm )
        self.label_condition.grid( row=1 , column=0 , columnspan=3 )

        self.label_temp_c = Label( frm )
        self.label_temp_c.grid( row=2 , column=0 )

        self.label_temp_f = Label( frm )
        self.label_temp_f.grid( row=2 , column=1 , columnspan= 2 )
          
    def get_foreecast( self , query ):
        if self.api is not None:
            thr = threading.Thread( target = self.api.fetch_forecast , args=( query , self.update_widgets , ) )
            thr.start()
    
    def update_widgets( self , status , data ):
        if status:
            condition_text = 'The weather condition at {0} is: {1}'.format( 
                data['location'][ 'name' ], 
                data['current'][ 'condition' ][ 'text' ]
            )
            self.label_condition.config( text=condition_text )
            self.label_temp_c.config( text='{} °C'.format( str( data['current'][ 'temp_c' ] ) ) )
            self.label_temp_f.config( text='{} °F'.format( str( data['current'][ 'temp_f' ] ) ) )
        else:
            self.label_condition.config( text='Ooops, something went wrong. The API response is:\n{}'.format( data ) )
            self.label_temp_c.config( text='' )
            self.label_temp_f.config( text='' )

##################
# MAIN APP CLASS
##################
class App( Tk ):
    api = None
    def __init__( self ):
        super().__init__()
        
        # Set up API
        self.api = Weather_API()

        # Set up App window
        self.geometry( '400x400' )
        self.title( 'Weather App' )
        self.columnconfigure( 0 , weight=1 )
        self.create_frames( )
    
    def create_frames( self ):
        # Create time frame
        def show_time( label:object ):
            label.config( text = strftime( '%H:%M:%S %p' ) )
            label.after( 1000 , show_time , label ) # recursive call every 1000ms

        header = Frame( self )
        header.grid( )
        time_label = Label( header , font=( 'Arial' , 25 ) )
        time_label.grid( row=0 , column=0 )
        show_time( time_label ) # start lable update loop

        # Create all weather app frames
        main = Frame( self )
        help     = Help_Frame(     main , [ None , None ] )
        api_key  = API_Key_Frame(  main , [ None , None ] )
        forecast = Forecast_Frame( main , [ None ] , self.api )
        help.set_nav_frame( 0 , forecast )
        help.set_nav_frame( 1 , api_key  )
        api_key.set_nav_frame( 0 , forecast )
        api_key.set_nav_frame( 1 , help )
        forecast.set_nav_frame( 0 , help )

        # Render initial frame depending on if there is API Key file or not
        if ( self.api is not None ) and self.api.has_API_Key():
            forecast.render() # forecast
        else:
            api_key.render()

##################
# MAIN APP RUN
##################
if __name__ == "__main__":
    app = App()
    app.mainloop()
