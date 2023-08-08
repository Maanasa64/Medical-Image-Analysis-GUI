from tkinter import *

root = Tk()

# any gui has a window. we need to create a window

#label wdget
myLabel = Label(root, text="Hello World")


#pack the text on the screen. "shoving the text on the screen" 
myLabel.pack()

#we need an event loop. it is always looping 
root.mainloop()

#RUN IN COMMAND LINE
