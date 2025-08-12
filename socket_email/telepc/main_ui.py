from tkinter import  Canvas, Button, PhotoImage


import os
import sys
def abs_path(file_name):
    file_name = 'assets\\' + file_name
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, file_name)

class Main_UI(Canvas):
    def __init__(self, parent):
        Canvas.__init__(self, parent)
        self.configure(
            #window,
            bg = "#FFFFFF",
            height = 600,
            width = 1000,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )
        self.place(x = 0, y = 0)
        self.image_image_1 = PhotoImage(
            file=abs_path("image_1.png"))
        self.image_1 = self.create_image(
            500.0,
            300.0,
            image=self.image_image_1
        )
        
        self.image_image_2 = PhotoImage(
            file=abs_path("image_2.png"))
        self.image_2 = self.create_image(
            466.0,
            323.0,
            image=self.image_image_2
        )
        self.button_image_1 = PhotoImage(
            file=abs_path("button_1.png"))
        self.button_1 = Button(self,
            image=self.button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_1 clicked"),
            relief="flat"
        )
        self.button_1.place(
            #x=727.0,
            #y=72.0,
            x=727.0,
            y=20.0,
            width=120.0,
            height=120.0
        )
        
        self.button_image_2 = PhotoImage(
            file=abs_path("button_2.png"))
        self.button_2 = Button(self,
            image=self.button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_2 clicked"),
            relief="flat"
        )
        self.button_2.place(
            #x=552.0,
            #y=251.0,
            x=552.0,
            y=173.0,
            width=120.0,
            height=120.0
        )


        self.button_image_3 = PhotoImage(
            file=abs_path("button_3.png"))
        self.button_3 = Button(self,
            image=self.button_image_3,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_3 clicked"),
            relief="flat"
        )
        self.button_3.place(
            #x=727.0,
            #y=251.0,
            x=727.0,
            y=173.0,
            width=120.0,
            height=120.0
        )
        
        self.button_image_4 = PhotoImage(
            file=abs_path("button_4.png"))
        self.button_4 = Button(self,
            image=self.button_image_4,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        self.button_4.place(
            #x=552.0,
            #y=430.0,
            x=552.0,
            y=327.0,
            width=120.0,
            height=120.0
        )

        self.button_image_5 = PhotoImage(
            file=abs_path("button_5.png"))
        self.button_5 = Button(self,
            image=self.button_image_5,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_5 clicked"),
            relief="flat"
        )
        self.button_5.place(
            #x=727.0,
            #y=430.0,
            x=727.0,
            y=327.0,
            width=120.0,
            height=120.0
        )
        
        self.button_image_6 = PhotoImage(
            file=abs_path("button_6.png"))
        self.button_6 = Button(self,
            image=self.button_image_6,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_6 clicked"),
            relief="flat"
        )
        self.button_6.place(
            x=130.2931671142578,
            y=448.287109375,
            width=247.55702209472656,
            height=47.96087646484375
        )
        
        self.button_image_7 = PhotoImage(
            file=abs_path("button_7.png"))
        self.button_7 = Button(self,
            image=self.button_image_7,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_7 clicked"),
            relief="flat"
        )
        self.button_7.place(
            #x=552.0,
            #y=72.0,
            x=552.0,
            y=20.0,
            width=120.0,
            height=120.0
        )
        
        self.button_image_8 = PhotoImage(
            file=abs_path("button_8.png"))
        self.button_8 = Button(self,
            image=self.button_image_8,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_7 clicked"),
            relief="flat"
        )
        self.button_8.place(
            x=639.0,
            y=466.0,
            width=120.0,
            height=120.0
        )

