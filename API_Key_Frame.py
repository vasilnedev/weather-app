"""
    The API_Key_Frame inherits Nav_Frame. It shows instructions and:
        * shows dialog to set/update API Key value and to save it
        * shows two navigation buttons to 'Get Weather' and 'Help'
        * uses Weather_API to set/change the API Key
"""
from tkinter   import *  # GUI framnework
from Nav_Frame import Nav_Frame # Basic navigable frame class
from Web_API   import Web_API   # Basic web API class

class API_Key_Frame( Nav_Frame ):
    def __init__( self , target:object, nav_frames={}, data_apis={} ):
        super().__init__( target , nav_frames , data_apis )

    # Overwrite Nav_Frame's method
    def widgets( self ):
        # instructions to display
        instructions = '''

This application requires an API Key from 

        www.weartherapi.com

Please visit the site and read the documentation. 

Once you have an API Key, use this form 
to save it and use this application.

'''
        Label(  self , text=instructions ).grid( row=0 , column=0 , columnspan=2 )

        # API Key dialog
 
        weather_api = self.data_apis[ 'Weather API' ] # select API
        
        API_Key = StringVar( )
        API_Key.set( weather_api.get_API_Key( ) )
        query_entry = Entry( self , textvariable = API_Key , width=40 )
        query_entry.grid( row=1 , column=0 , columnspan=2 )
        query_entry.focus()

        Button( self , text="Save API Key", 
            command = lambda: 
                    weather_api.save_API_Key( query_entry.get() )
        ).grid( row=2 , column=0 , columnspan=2 )
 
        # Navigation buttons
        Button( self , text="Get Weather", command = lambda: self.navigate_to( 'Get Weather' ) ).grid( row=3 , column=0 )
        Button( self , text="Help"       , command = lambda: self.navigate_to( 'Help' )        ).grid( row=3 , column=1 )
