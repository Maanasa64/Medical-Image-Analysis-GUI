from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("test image resized")
root.geometry("800x500")


# open image
my_pic = Image.open("images/image.tif")

# resize image
resized = my_pic.resize((300,225), Image.ANTIALIAS)


new_pic = ImageTk.PhotoImage(resized)
my_label = Label(root, image=new_pic)
my_label.pack(pady=20)

root.mainloop()

#RUN IN COMMAND LINE

