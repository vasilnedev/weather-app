from tkinter import *
from tkinter import ttk
from time    import strftime

class Basic_Frame():
    container = None
    title = 'Basic Frame'
    next_frame = None
    def __init__( self , container , title , next_frame ):
        self.container = container
        self.title = title
        self.next_frame = next_frame
    
    def set_next_frame( self , next_frame ):
        self.next_frame = next_frame

    def widgets( self , frm ):
        Label(  frm , text=self.title ).grid( row=0 , column=0 )
        Button( frm , text="Next", 
            command = self.next_frame.render
        ).grid( row=0 , column=1 )

    def render( self ):
        # Check if root is set
        if self.container is not None:
            # clear container
            for child in self.container.winfo_children():
                child.destroy()
            # Create new Frame
            frm = Frame( self.container )
            frm.grid()
            self.widgets( frm )   # Add widgets
            self.container.grid() # Show the container ( frame_main )


class App( Tk ):
    def __init__( self ):
        super().__init__()
        self.geometry( '400x400' )
        self.title( 'App Title' )
        self.columnconfigure( 0 , weight=1 )
        self.create_frames( )
    
    def create_frames( self ):
        def show_time( label:object ):
            label.config( text = strftime( '%H:%M:%S %p' ) )
            label.after( 1000 , show_time , label ) # recursive call every 1000ms

        header = Frame( self )
        header.grid( )
        time_label = Label( header , font=( 'Arial' , 25 ) )
        time_label.grid( row=0 , column=0 )
        show_time( time_label ) # start lable update loop

        # Create main frame - show sub-frames
        main = Frame( self )
        bf1 = Basic_Frame( main , 'Frame 1' , None )
        bf2 = Basic_Frame( main , 'Frame 2' , bf1 )
        bf1.set_next_frame( bf2 )
        bf1.render() # render the first frame


##################
# MAIN APP
##################
if __name__ == "__main__":
    app = App()
    app.mainloop()
