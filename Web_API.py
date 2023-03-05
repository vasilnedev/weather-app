"""
    Web_API is a generic data class - to be inherited by other data classes. 
    
    Most API services use API keys for access control, so this class
    has functionality to store an API Key.

    This class: 
        * stores API Key, url and data variables
        * loads/saves API Key from file
"""
import logging

class Web_API():
    API_key_file = ''
    API_Key      = ''
    url          = ''
    data         = None

    def __init__( self , url='' , API_key_file='' ):
        self.url = url
        self.API_key_file = API_key_file
        if API_key_file != '':
            self.load_API_Key()

    def get_data( self ):
        return self.data

    def get_API_Key( self ):
        return self.API_Key

    def has_API_Key( self ):
        return ( self.API_Key != '' )

    def load_API_Key( self ):
        try:
            f = open( self.API_key_file , 'r' )
            self.API_Key = f.read()
            f.close()
        except Exception:
            logging.warning( 'File reading exception in Web_API!' )

    def save_API_Key( self , key:str ):
        self.API_Key = key
        try:
            f = open( self.API_key_file , 'w' )
            f.write( key )
            f.close()
        except Exception:
            logging.warning( 'File writeing exception in Web_API!' )

    # An abstract method that shall be rewritten by all inheriting classes
    def fetch_data( self , query='' , callback=None ):
        logging.warning( 'Web_API fetch_data method not implemented!' )
