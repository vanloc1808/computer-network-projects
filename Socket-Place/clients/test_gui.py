import tkinter as tk
import tkinter.ttk as ttk
from functools import partial

window = tk.Tk()
window.title("Let's solo Yasuo")

"""
label = tk.Label(
    text="Hello, Tkinter",
    foreground="white",  # Set the text color to white
    background="black",  # Set the background color to black
    width = 10,
    height = 10
)
label.pack()

button = tk.Button(
    text="Click me!",
    width = 25,
    height = 5,
    background="blue",
    foreground="yellow",
)
button.pack()

entry = tk.Entry(
    width = 25,
    background="blue",
    foreground="yellow"
)
entry.pack()

# print the content of the entry
entry.bind("<Return>", lambda event: print(entry.get()))

text_box = tk.Text()
text_box.pack()
text_box.bind("<Return>", lambda event: print(text_box.get("1.0", "end-1c")))


frame = tk.Frame()
label = tk.Label(master=frame)
label.pack()

frame_a = tk.Frame()
frame_b = tk.Frame()

label_a = tk.Label(master=frame_a, text="I'm in Frame A")
label_a.pack()

label_b = tk.Label(master=frame_b, text="I'm in Frame B")
label_b.pack()

frame_b.pack()
frame_a.pack()

window.mainloop()


border_effects = {
    "flat": tk.FLAT,
    "sunken": tk.SUNKEN,
    "raised": tk.RAISED,
    "groove": tk.GROOVE,
    "ridge": tk.RIDGE,
}

for relief_name, relief in border_effects.items():
    frame = tk.Frame(master = window, relief = relief, borderwidth = 5)
    frame.pack(side = tk.LEFT)
    label = tk.Label(master = frame, text = relief_name)
    label.pack()
"""

def handle_click(event):
    print("The button was clicked!")

def print_name():
    print("Hello my name is Python")

def print_name_event(name):
    print("Hello my name is " + name)

button1 = tk.Button(text="Button 1")
button1.pack()
button1.bind("<Button-1>", handle_click)

button2 = tk.Button(text="Button 2")
button2.pack()
button2.bind("<Button-1>", handle_click)

button3 = tk.Button(text="Button 3", command = print_name)
button3.pack()
button3.bind("<Button-1>", handle_click)

button4 = tk.Button(text="Button 4", command=partial(print_name_event, "Python"))
button4.bind("<Button-1>")
button4.pack()

window.mainloop()