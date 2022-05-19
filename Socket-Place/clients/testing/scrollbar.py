from tkinter import *

root = Tk()
scrollbar = Scrollbar(root)
scrollbar.pack( side = RIGHT, fill = Y )

mylist = Listbox(root, yscrollcommand = scrollbar.set )
for line in range(100):
   # frm = Frame(master=root)
   # frm.pack()
   # lbl = Label(master=frm, text='This is frame ' + str(line))
   mylist.insert(END, "This is line number " + str(line))
   #mylist.insert(END, lbl)

mylist.pack( side = LEFT, fill = BOTH )
scrollbar.config( command = mylist.yview )

mainloop()