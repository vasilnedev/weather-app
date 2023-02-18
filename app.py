from tkinter import *
from tkinter import ttk
from time    import strftime

# GUI form
def gui_form( parent:object ):

    # Help function to update every second a time label
    def my_time( label:object ):
        label.config( text= strftime( '%H:%M:%S %p | %x' ) )
        label.after( 1000 , my_time , label )
    
    def get_forecast( ):
        print( "get forecast" )

    frm = ttk.Frame( parent , padding=5 )
    frm.grid()
    
    ttk.Label(  frm, text="Weather App").grid( row=0 , column=0 , columnspan=2 )

    time_label = ttk.Label( frm )
    time_label.grid( row=1 , column=0 , columnspan=2 )
    my_time( time_label ) # start lable update loop

    ttk.Label(  frm, text="Longitude" ).grid( row=2 , column=0 )
    ttk.Label(  frm, text="Latitude"  ).grid( row=2 , column=1 )

    longitude = ttk.Entry( frm , width=10 )
    longitude.grid( row=3 , column=0 )
    latitude  = ttk.Entry( frm , width=10 )
    latitude.grid( row=3 , column=1 )
    
    ttk.Button( frm, text="Get Forecast", command=get_forecast ).grid( row=4 , column=0 )
    ttk.Button( frm, text="Quit", command=parent.destroy ).grid( row=4 , column=1 )


##################
# MAIN APP
##################
root = Tk()

gui_form( root )

root.mainloop()
