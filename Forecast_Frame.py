"""
    The Forecast_Frame inherits Nav_Frame. It:
        * shows dialog to query Weather API 
        * shows the weather information
        * uses Weather_API to fetch weather information
"""
from tkinter import *  # GUI framnework
import threading # to fetch data on the background - not blocking the app
from datetime import datetime

from Nav_Frame import Nav_Frame  # Basic navigable frame class
from Chart_Window import Chart_Window

class Forecast_Frame( Nav_Frame ):
    # Parameter
    query = 'auto:ip'
    # Refs to widgets
    label_condition = None
    label_temp_c    = None
    label_temp_f    = None
    label_icon      = None
    button_get      = None
    forecast_frame  = None
    # windows
    chart_window    = None

    def __init__( self , target:object, nav_frames={}, data_apis={} ):
        super().__init__( target , nav_frames , data_apis )

    def get_query( self ):
        return self.query

    def show_chart( self ):
        def on_closing():
            self.chart_window.destroy()
            self.chart_window = None
        # Configure the chart window
        if self.chart_window is None:
            self.chart_window = Chart_Window(
                title='Weather Chart', 
                geometry='700x400', 
                data = self.data_apis[ 'Weather API' ].get_data() 
            ) 
            self.chart_window.plot_chart()
            self.chart_window.protocol("WM_DELETE_WINDOW", on_closing )

    # Overwrite Nav_Frame's method
    def widgets( self ):
        weather_api = self.data_apis[ 'Weather API' ] # select API

        # Query dialog
        entry_query = Entry( self )
        entry_query.grid( row=0 , column=0 )
        entry_query.focus()
        self.button_get = Button( self , text="Get Weather" , bg='#FF781F' , fg='white' ,
            command = lambda: self.get_forecast( entry_query.get() ) 
        )
        self.button_get.grid( row=0 , column=1 )
        Button( self , text="Chart", bg='#FF781F' , fg='white' , 
            command = self.show_chart 
        ).grid( row=0 , column=2 )
        Button( self , text="Help" , command = lambda: self.navigate_to( 'Help' ) ).grid( row=0 , column=3 )
        
        # Crrent condition and forecast placeholders
        self.label_condition = Label( self )
        self.label_condition.grid( row=1 , column=0 , columnspan=4 )

        self.label_icon = Label( self )
        self.label_icon.grid( row=2 , column=0 , columnspan=2 )

        self.label_temp_c = Label( self )
        self.label_temp_c.grid( row=2 , column=1 )

        self.label_temp_f = Label( self )
        self.label_temp_f.grid( row=2 , column=2 )

        self.forecast_frame = Frame( self )
        self.forecast_frame.grid( row=3 , column=0 , columnspan=4 )

        # If data is available populate the widgets or start loading from API
        if weather_api.get_data() is not None:
            self.update_widgets( self.query, True , weather_api.get_data() )
        else:
            # Get default location from auto IP address
            self.button_get[ 'state' ] = 'disabled'
            thr = threading.Thread( target = weather_api.fetch_data , args=( self.query , self.update_widgets , ) )
            thr.start()

    # Button event handler for sending a query to the Weather API      
    def get_forecast( self , query ):
        # Clear own widgets
        self.label_condition.config( text='Loading data ...' )
        self.label_temp_c.config( text='' )
        self.label_temp_f.config( text='' )
        self.label_icon.config( image = '' )
        self.button_get[ 'state' ] = 'disabled'
        for child in self.forecast_frame.winfo_children():
            child.destroy()

        # fetch data in a Thread and call update_widgets when ready
        weather_api = self.data_apis[ 'Weather API' ] # select API
        thr = threading.Thread( target = weather_api.fetch_data , args=( query , self.update_widgets , ) )
        thr.start()

    # Callback function to be called when weather data is available
    def update_widgets( self , query , status , data ):
        self.button_get[ 'state' ] = 'normal'
        if status:
            self.query = query
            condition_text = 'The weather condition in {0} is:\n {1} at local time {2}'.format( 
                data[ 'location' ][ 'name' ], 
                data[ 'current'  ][ 'condition' ][ 'text' ],
                data[ 'location' ][ 'localtime' ]
            )
            self.label_condition.config( text=condition_text )
            self.label_temp_c.config( text='{}°C'.format( str( data['current'][ 'temp_c' ] ) ) , font=( 'Arial' , 20 ) )
            self.label_temp_f.config( text='{}°F'.format( str( data['current'][ 'temp_f' ] ) ) , font=( 'Arial' , 20 ) )

            # Display icon of current condition
            weather_api = self.data_apis[ 'Weather API' ] # select API
            self.label_icon.config( image = weather_api.get_icon( str( data['current'][ 'condition' ][ 'icon' ] ) ) )

            # Display forecast table
            Label( self.forecast_frame , text='―――――― 5 days forecast ――――――' , font=( 'Arial' , 14 ) ).grid( row=0 , column=0 , columnspan=4 )
            days=[ 'Mon' , 'Tue' , 'Wed' , 'Thu' , 'Fri' , 'Sat' , 'Sun' ]
            row = 1
            for day in data['forecast']['forecastday']:
                dt = datetime.strptime( day['date'] , '%Y-%m-%d' )
                wd = dt.weekday()
                Label( self.forecast_frame , 
                    text = '{0}\n{1}'.format( day['date'] , day['day']['condition']['text'] ) 
                ).grid( row=row , column=0 )
                Label( self.forecast_frame , text = ' {} '.format( days[ wd ] ) , font=( 'Arial' , 14 ) ).grid( row=row , column=1 )
                Label( self.forecast_frame , 
                    image = weather_api.get_icon( str( day['day']['condition']['icon'] ) ) 
                ).grid( row=row , column=2 )
                Label( self.forecast_frame ,
                    text='{0}°C\n{1}°F'.format( day['day']['avgtemp_c'] , day['day']['avgtemp_f'] )
                ).grid( row=row , column=3 )
                row += 1

        else:
            self.label_condition.config( text='Ooops, something went wrong. The API response is:\n{}'.format( data ) )
