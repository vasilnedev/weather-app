"""
    Weather_API inherits Web_API and adds specific functionality to store icons.

    It's based on the www.weatherapi.com documentation.
"""

from PIL     import Image , ImageTk # Image library for the icons
from io      import BytesIO         # needed to store image data from internet
import requests                     # Internet request library

from Web_API import Web_API         # Basic internet API class

class Weather_API( Web_API ):
    icons = {} # Application specific data - in addition to the data of Web_API class 

    def __init__( self , url, API_key_file='' ):
        super().__init__( url , API_key_file )

    def get_icon( self , icon_key ):
        if icon_key in self.icons:
            return self.icons[ icon_key ]
        else:
            return '' # Note that to clear image in label need to set image=''

    def fetch_icon( self , icon_key ):
        if icon_key not in self.icons or self.icons[ icon_key ] is None:
            res = requests.get( 'http:' + icon_key )
            res.close()
            if res.status_code == 200:
                image_icon = Image.open( BytesIO( res.content ) )
                self.icons[ icon_key ] = ImageTk.PhotoImage( image_icon )
            else: 
                self.icons[ icon_key ] = None
            

    # Overwrite Web_API method
    def fetch_data( self , query:str , callback:object ):
        # Send API request like:
        # url ? key = < API KEY > & q = London & days = 7 & aqi=no & alerts = no
        # For full documentation visit https://www.weatherapi.com site
        params = {
            'key': self.API_Key, 
            'q': query,
            'days': 5,
            'aqi': 'no',   # aqi = air quality
            'alerts':'no'
        }
        res = requests.get( self.url , params=params )
        res.close()
        # Return data and call the callback function with arguments: status:bool and data:object
        if res.status_code == 200: # HTTP status code 200 - OK
            self.data = res.json()
            # Fetch current and forecast icons
            self.fetch_icon( str( self.data['current'][ 'condition' ][ 'icon' ] ) )
            for day in self.data['forecast']['forecastday']:
                self.fetch_icon( str( day['day']['condition'][ 'icon' ] ) )

            callback( query , True, self.data )
        else:
            callback( query , False, res.reason )
