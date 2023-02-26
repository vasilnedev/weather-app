from tkinter import *
from tkinter import ttk
from time    import strftime

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
    def __init__( self ,  container , nav_frames ):
        super().__init__( container , nav_frames )

    def widgets( self , frm ):
        Button( frm , text="Help" , command = lambda: self.nav_frame( 0 ) ).grid( row=1 , column=1 )

##################
# MAIN APP CLASS
##################
class App( Tk ):
    def __init__( self ):
        super().__init__()
        self.geometry( '400x400' )
        self.title( 'App Title' )
        self.columnconfigure( 0 , weight=1 )
        self.create_frames( )
    
    def create_frames( self ):
        def show_time( label:object ):
            label.config( text = strftime( '%H:%M:%S %p' ) )
            label.after( 1000 , show_time , label ) # recursive call every 1000ms

        header = Frame( self )
        header.grid( )
        time_label = Label( header , font=( 'Arial' , 25 ) )
        time_label.grid( row=0 , column=0 )
        show_time( time_label ) # start lable update loop

        # Create main frame - show sub-frames
        main = Frame( self )
        help     = Help_Frame(     main , [ None , None ] )
        api_key  = API_Key_Frame(  main , [ None , None ] )
        forecast = Forecast_Frame( main , [ None ] )
        help.set_nav_frame( 0 , forecast )
        help.set_nav_frame( 1 , api_key  )
        api_key.set_nav_frame( 0 , forecast )
        api_key.set_nav_frame( 1 , help )
        forecast.set_nav_frame( 0 , help )
        forecast.render() # render the first frame

##################
# MAIN APP RUN
##################
if __name__ == "__main__":
    app = App()
    app.mainloop()
