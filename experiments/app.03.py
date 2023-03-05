from tkinter import *
from tkinter import ttk
from time    import strftime
from turtle import color
from PIL     import Image , ImageTk
from io      import BytesIO
import requests
import threading

class Weather_API():
    API_key_file = 'weatherapi.key'
    url = "http://api.weatherapi.com/v1/forecast.json"
    API_Key = None
    data = None
    icons = {}
    def __init__( self ):
        self.load_API_Key()

    def get_data( self ):
        return self.data

    def get_icon( self , icon_key ):
        if icon_key in self.icons:
            return self.icons[ icon_key ]
        else:
            return '' # Note that to clear image in label need to set image=''

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
        except Exception: pass

    def get_API_Key( self ):
        return self.API_Key

    def has_API_Key( self ):
        return ( self.API_Key is not None )

    def fetch_icon( self , icon_key ):
        if icon_key not in self.icons or self.icons[ icon_key ] is None:
            res = requests.get( 'http:' + icon_key )
            if res.status_code == 200:
                image_icon = Image.open( BytesIO( res.content ) )
                self.icons[ icon_key ] = ImageTk.PhotoImage( image_icon )
            else: 
                self.icons[ icon_key ] = None

    def fetch_forecast( self , query:str , callback:object ):
        # Send API request like:
        # http://api.weatherapi.com/v1/current.json?key=< API KEY >&q=London&aqi=no
        # For full documentation visit https://www.weatherapi.com site
        params = {
            'key': self.API_Key, 
            'q': query,
            'days':7,
            'aqi': 'no',   # To get air quality data or not
            'alerts':'no'
        }
        res = requests.get( self.url , params=params )  
        # Return data
        if res.status_code == 200: # HTTP status code 200 - OK
            self.data = res.json()
            self.fetch_icon( str( self.data['current'][ 'condition' ][ 'icon' ] ) )
            callback( True, self.data )
        else:
            callback( False, res.reason )

class Nav_Frame():
    container = None
    nav_frames = []
    data_apis  = []

    def __init__( self , container:object , nav_frames:list , data_apis:list ):
        self.container  = container
        self.nav_frames = nav_frames
        self.data_apis  = data_apis
    
    def set_nav_frames( self , nav_frames:list ):
        self.nav_frames = nav_frames

    def render_nav_frame( self , index:int ):
        try:
            self.nav_frames[ index ].render()
        except Exception: pass

    def get_data_api( self , index:int ):
        if index < len( self.data_apis ):
            return self.data_apis[ index ]
        else:
            return None

    def widgets( self , frm:object ): pass # This method shall be rewritten by all child classes

    def render( self ):
        # Check if container is set
        if self.container is not None:
            # clear container
            for child in self.container.winfo_children():
                child.destroy()
            # Create new Frame
            frm = Frame( self.container )
            frm.grid()
            self.widgets( frm )   # Add widgets
            self.container.grid() # Show the container ( frame_main )

class Help_Frame( Nav_Frame ):
    def __init__( self ,  container:object , nav_frames:list , data_apis:list ):
        super().__init__( container , nav_frames , data_apis )

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
        Button( frm , text="Get Weather", command = lambda: self.render_nav_frame( 0 ) ).grid( row=1 , column=0 )
        Button( frm , text="API Key" , command = lambda: self.render_nav_frame( 1 ) ).grid( row=1 , column=1 )

class API_Key_Frame( Nav_Frame ):
    def __init__( self ,  container:object , nav_frames:list , data_apis:list ):
        super().__init__( container , nav_frames , data_apis )

    def widgets( self , frm ):
        instructions = '''

This application requires an API Key from 

           www.weartherapi.com

Please visit the site and read the documentation. 

Once you have an API Key, use this form 
to save it and use this application.

'''
        Label(  frm , text=instructions ).grid( row=0 , column=0 , columnspan=2 )

        API_Key = StringVar( )
        API_Key.set( self.get_data_api( 0 ).get_API_Key() )
        query_entry = Entry( frm , textvariable = API_Key , width=40 )
        query_entry.grid( row=1 , column=0 , columnspan=2 )
        query_entry.focus()

        Button( frm, text="Save API Key", 
            command = lambda: 
                    self.get_data_api( 0 ).save_API_Key( query_entry.get() )
        ).grid( row=2 , column=0 , columnspan=2 )

        Button( frm , text="Get Weather", command = lambda: self.render_nav_frame( 0 ) ).grid( row=3 , column=0 )
        Button( frm , text="Help"    , command = lambda: self.render_nav_frame( 1 ) ).grid( row=3 , column=1 )

class Forecast_Frame( Nav_Frame ):
    label_condition = None
    label_temp_c    = None
    label_temp_f    = None
    label_icon      = None
    button_get      = None

    def __init__( self ,  container:object , nav_frames:list , data_apis:list ):
        super().__init__( container , nav_frames , data_apis )

    def widgets( self , frm ):
        query = Entry( frm )
        query.grid( row=0 , column=0 )
        query.focus()
        self.button_get = Button( frm , text="Get Weather",
            command = lambda: self.get_forecast( query.get() ) 
        )
        self.button_get.grid( row=0 , column=1 )
        Button( frm , text="Help" , 
            command = lambda: self.render_nav_frame( 0 ) 
        ).grid( row=0 , column=2 )
        
        self.label_condition = Label( frm )
        self.label_condition.grid( row=1 , column=0 , columnspan=3 )

        self.label_icon = Label( frm )
        self.label_icon.grid( row=2 , column=0 )

        self.label_temp_c = Label( frm )
        self.label_temp_c.grid( row=2 , column=1 )

        self.label_temp_f = Label( frm )
        self.label_temp_f.grid( row=2 , column=2 )

        if self.get_data_api( 0 ).get_data() is not None:
            self.update_widgets( True , self.get_data_api( 0 ).get_data() )
          
    def get_forecast( self , query ):
        if self.get_data_api( 0 ) is not None:
            # Clear widgets
            self.label_condition.config( text='Loading data ...' )
            self.label_temp_c.config( text='' )
            self.label_temp_f.config( text='' )
            self.label_icon.config( image = '' )
            self.button_get[ 'state' ] = 'disabled'
            # fetch data and call update_widgets when ready
            thr = threading.Thread( target = self.get_data_api( 0 ).fetch_forecast , args=( query , self.update_widgets , ) )
            thr.start()
        else:
            pass # Handle case when there is no data API
    
    def update_widgets( self , status , data ):
        self.button_get[ 'state' ] = 'normal'
        if status:
            condition_text = 'The weather condition in {0} is:\n {1} at local time {2}'.format( 
                data[ 'location' ][ 'name' ], 
                data[ 'current'  ][ 'condition' ][ 'text' ],
                data[ 'location' ][ 'localtime' ]
            )
            self.label_condition.config( text=condition_text )
            self.label_temp_c.config( text='{} °C'.format( str( data['current'][ 'temp_c' ] ) ) )
            self.label_temp_f.config( text='{} °F'.format( str( data['current'][ 'temp_f' ] ) ) )
            self.label_icon.config( image = self.get_data_api( 0 ).get_icon( str( data['current'][ 'condition' ][ 'icon' ] ) ) )
        else:
            self.label_condition.config( text='Ooops, something went wrong. The API response is:\n{}'.format( data ) )

##################
# MAIN APP CLASS
##################
class App_Window( Tk ):
    imageTk_icon = None
    data_api = None
    def __init__( self , title:str , geometry:str ):
        super().__init__()
        
        # Set up data API
        self.data_api = Weather_API()

        # Set up app window
        self.geometry( geometry )
        self.title( title )
        self.columnconfigure( 0 , weight=1 )
    
    def render( self ):
        # Create window layout
        header_frame = Frame( self )
        header_frame.grid( row=0 , column=0 )

        main_frame = Frame( self )
        main_frame.grid( row=1 , column=0 )

        # Create header frame content and render it
        image_icon   = Image.open( 'logo.png' )
        self.imageTk_icon = ImageTk.PhotoImage( image_icon )
        Label( header_frame , image=self.imageTk_icon ).grid( row=0 , column=0 )
        
        time_label = Label( header_frame , font=( 'Arial' , 18 ) )
        time_label.grid( row=0 , column=1 )
        def show_time( label:object ):
            label.config( text = '   ' + strftime( '%H:%M:%S %p' ) )
            label.after( 1000 , show_time , label ) # recursive call every 1000ms
        show_time( time_label ) # start lable update loop

        # Create main frame content and link to APIs
        help_nav_frame = Help_Frame( main_frame , [] , [] )
        api_key_nav_frame = API_Key_Frame(   main_frame , [] , [ self.data_api ] )
        forecast_nav_frame = Forecast_Frame( main_frame , [] , [ self.data_api ] )
        # Set navigations
        help_nav_frame.set_nav_frames(     [ forecast_nav_frame , api_key_nav_frame ] )
        api_key_nav_frame.set_nav_frames(  [ forecast_nav_frame , help_nav_frame ] )
        forecast_nav_frame.set_nav_frames( [ help_nav_frame ] )


        # Navigate depending on if API Key file exists
        if ( self.data_api is not None ) and self.data_api.has_API_Key():
            forecast_nav_frame.render()
        else:
            api_key_nav_frame.render()

##################
# MAIN APP RUN
##################
if __name__ == "__main__":
    app = App_Window( title='Weather App' , geometry='400x450' )
    app.render()
    app.mainloop()
