"""
    This module creates a Window to plot data received from Weather API. It shall be called from Forecast_Frame button.

    When started as a standalone app, it reads test data from json file
"""

# External modules
import json
from   datetime import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from   matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from   tkinter  import *  # GUI framework

class Chart_Window( Tk ):
    def __init__( self , title:str , geometry:str , data:dict ):
        super().__init__()

        # Set up app window
        self.geometry( geometry )
        self.title( title )
        self.attributes('-topmost',True)
        self.columnconfigure( 0 , weight=1 )
        self.data = data
    
    def plot_chart( self ):

        # Prepare data
        hour_data = []
        forecastday = self.data['forecast']['forecastday']
        wdays=[ 'Mon' , 'Tue' , 'Wed' , 'Thu' , 'Fri' , 'Sat' , 'Sun' ]
        i = 0
        for day in forecastday:
            for hour in day['hour']:
                dt_str = hour['time']
                dt_obj = datetime.strptime( dt_str, '%Y-%m-%d %H:%M')
                row = {
                    'text': hour['condition']['text'],
                    'icon': hour['condition']['icon'],
                    'hour': wdays[ dt_obj.weekday() ] + '\n' + str( dt_obj.hour ) + ':00'
                }
                for key, value in hour.items():
                    if key != 'condition':
                        row[key] = value
                hour_data.append( row )
            i += 1
        
        # Create DataFrame
        df = pd.DataFrame( hour_data ) 

        # Plot chart   
        figure = plt.Figure( figsize=(10,7) , dpi=100 )
        ax = figure.add_subplot( 111 )
        chart_type = FigureCanvasTkAgg( figure , self )
        chart_type.get_tk_widget().pack()
        df.plot.area( x = 'hour' , y = 'cloud', ax = ax , color=( '#B0B0C0' ) ) 
        df.plot( x = 'hour' , y = 'temp_c' , ax = ax , secondary_y = True , color=( '#FF781F' ) ) 

if __name__ == "__main__":
    with open('forecast.json','r') as f:
        test_data = json.loads(f.read())

    chart = Chart_Window( title='Test Weather Chart' , geometry='700x400' , data=test_data ) # Configure the app
    chart.plot_chart()
    chart.mainloop()    # Display the app window
