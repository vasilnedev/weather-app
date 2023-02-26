"""
    Learning/demo application to experiment GUI
    with threading
"""
from   tkinter import *
from   tkinter import ttk
from   time    import strftime
import time
import threading

# A button event handler that delays for 5 seconds
def slow_button( name:str ):
    print( f'Slow button {name} - start' )
    time.sleep( 5 )
    print( f'Slow button {name} - stop' )

# A button event handler that delays for 0.5 seconds
def fast_button():
    print( 'Fast button - start' )
    time.sleep( 0.5 )
    print( 'Fast button - stop' )

# A button event handler that delays for 5 seconds
def slow_threading_button():
    thr = threading.Thread( target = slow_button, args=( 'threading', ) )
    thr.start()

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
time_label.grid( row=0 , column=1 , columnspan=2 )
show_time( time_label ) # Start loop to update the time

ttk.Button( frm , 
    text="Slow button", 
    command = lambda: slow_button( 'no threading' )
).grid( row=1 , column=0 )

ttk.Button( frm , 
    text="Fast button", 
    command = fast_button 
).grid( row=1 , column=1 )

ttk.Button( frm , 
    text="Slow button\nwith threading", 
    command = slow_threading_button 
).grid( row=1 , column=2 )
# Frame end

root.mainloop() # Show the graphic window
