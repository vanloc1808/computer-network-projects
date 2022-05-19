from tkinter import *
from PIL import ImageTk, Image, ImageFont, ImageDraw
import os

root = Tk()
frame = Frame(root)
frame.pack()
load = Image.open('C:\\Users\\admin\\AppData\\Local\\Temp/oyhmnkwkewui.jpg')
size = 256, 256
load = load.resize(size, Image.ANTIALIAS)
photo = ImageTk.PhotoImage(load)
label = Label(master=frame, image=photo)
label.image = photo
label.pack()
label1 = Label(master=frame, text='Hello')
label1.pack()

frame1 = Frame(root)
frame1.pack()
img_o = Image.open('C:\\Users\\admin\\AppData\\Local\\Temp/ddhzdpjwmurm.jpg')
img_o = img_o.resize(size, Image.ANTIALIAS)
img_l = ImageTk.PhotoImage(img_o)
img_label = Label(master = frame1, image=img_l)
img_label.image = img_l
img_label.pack()
txt_label = Label(master = frame1, text='Hello World')
txt_label.pack()

root.mainloop()