"""
    The Help_Frame inherits Nav_Frame. It shows instructions and:
        * shows two buttons - 'Get Weather' and 'API Key' to allow navigation
        * has no data sources
"""
from tkinter   import * # GUI framnework
from Nav_Frame import Nav_Frame # Basic navigable frame class

class Help_Frame( Nav_Frame ):
    def __init__( self ,
        target:object, nav_frames={}, data_apis={} ):
        super().__init__( target , nav_frames , data_apis )

    # Overwrite Nav_Frame's method
    def widgets( self ):
        # Help information to display
        instructions = '''

For detailed documentation about WeatherAPI visit:

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
        Label(  self , text=instructions ).grid( row=0 , column=0 , columnspan=2 )

        # Navigation buttons
        Button( self , text='Get Weather', command = lambda: self.navigate_to( 'Get Weather' ) ).grid( row=1 , column=0 )
        Button( self , text='API Key'    , command = lambda: self.navigate_to( 'API Key' )     ).grid( row=1 , column=1 )
