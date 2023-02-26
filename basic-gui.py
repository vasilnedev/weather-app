"""
    Learning/demo application to experiment GUI
    without threading
"""
from   tkinter import *
from   tkinter import ttk
from   time    import strftime
import time

# A button event handler that delays for 5 seconds
def slow_button( ):
    print( f'Slow button - start' )
    time.sleep( 5 )
    print( f'Slow button - stop' )

# A button event handler that delays for 0.5 seconds
def fast_button():
    print( 'Fast button - start' )
    time.sleep( 0.5 )
    print( 'Fast button - stop' )

# Help function to update the time label every second
# by making recursive calls
def show_time( label:object ):
    label.config( text = strftime( '%H:%M:%S %p' ) )
    label.after( 1000 , show_time , label ) # recursive call every 1000ms

##################
# MAIN APP
##################
root = Tk(  ) # Create graphic window
root.winfo_toplevel().title( 'Basic GUI' )

# Frame start
frm = ttk.Frame( root , padding=5 ) # Create a frame 
frm.grid() # Set grid layout

ttk.Label(  frm , text='Time:' ).grid( row=0 , column=0 )
time_label = ttk.Label(  frm , text='local time' )
time_label.grid( row=0 , column=1 )
show_time( time_label ) # Start loop to update the time

ttk.Button( frm , 
    text='Slow button', 
    command = slow_button
).grid( row=1 , column=0 )

ttk.Button( frm , 
    text='Fast button', 
    command = fast_button 
).grid( row=1 , column=1 )
# Frame end

root.mainloop() # Show graphic window
