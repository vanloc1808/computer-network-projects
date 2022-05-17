import tkinter as tk
import tkinter.ttk as ttk

from matplotlib.pyplot import text

window = tk.Tk()
window.title("Let's solo Yasuo")

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

window.mainloop()