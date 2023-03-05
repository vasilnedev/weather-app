"""
    Nav_Frame is a basic visual class - to be inherited by higher-level classes. It works like
    a playing card deck that show only one at a time and hides the others.
    It: 
        * creates a Tk Frame 
        * keeps dictionaries of other Nav_Frames and data APIs related to each frame
        * shows itself and hides the others on render event
"""
import logging
from   tkinter import *

class Nav_Frame( Frame ):
    nav_frames = {} # dictionary of linked Nav_Frames
    data_apis  = {} # dictionary of data APIs

    def __init__( self , target:object , nav_frames={} , data_apis={} ):
        super().__init__( target )
        self.nav_frames = nav_frames
        self.data_apis  = data_apis
    
    # Allow assigning nav_frames after creating an instance
    def set_nav_frames( self , nav_frames:dict ):
        self.nav_frames = nav_frames

    # An abstract method that shall be rewritten by all inheriting classes
    def widgets( self ): 
        logging.warning( 'Nav_Frame widgets method not implemented!' )

    def navigate_to( self , key:str ):
        if key in self.nav_frames:
            self.nav_frames[ key ].render()

    def render( self ):
        # Hide siblings and show self
        for sibling in self.master.winfo_children():
            if sibling is self: self.grid() # show frame
            else: sibling.grid_forget()     # hide frame
