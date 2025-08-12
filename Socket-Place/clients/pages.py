import tkinter as tk
from functools import partial
from PIL import ImageTk, Image

class Page(tk.Frame):
    def __init__(self, id, name, avt, size, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        load_avt = Image.open(avt)
        load_avt = load_avt.resize(size, Image.ANTIALIAS)
        photo_avt = ImageTk.PhotoImage(load_avt)

        lbl_avt = tk.Label(master=self, image=photo_avt)
        lbl_avt.image = photo_avt
        lbl_avt.pack()

        lbl_caption = tk.Label(master=self, text=name)
        lbl_caption.pack()

def create_first_frame(frames):
    frm_button = tk.Frame(master=frames[0])
    frm_button.pack(side='bottom')

    btn_next = tk.Button(master=frm_button, text='Hình kế', command=partial(show_middle_frame, frames, 1), height=5)
    btn_next.pack(pady=30, side='right')

def create_last_frame(frames):
    idx = len(frames) - 1

    frm_buttons = tk.Frame(master=frames[idx])
    frm_buttons.pack(side='bottom')
    btn_next = tk.Button(master=frm_buttons, text='Hình trước', command=partial(show_middle_frame, frames, idx - 1), height=5)
    btn_next.pack(pady=30, side='left')

def create_middle_frames(frames, i):
    frm_buttons = tk.Frame(master=frames[i])
    frm_buttons.pack(side='bottom')
    btn_next = tk.Button(master=frm_buttons, text='Hình trước', command=partial(show_middle_frame, frames, i - 1), height=5)
    btn_next.pack(pady=30, side='left')
    btn_prev = tk.Button(master=frm_buttons, text='Hìhh kế', command=partial(show_middle_frame, frames, i + 1), height=5)
    btn_prev.pack(pady=30, side='right')

def create_frames(frames):
    create_first_frame(frames)
    create_last_frame(frames)

    for i in range(1, len(frames) - 1, 1):
        create_middle_frames(frames, i)

def show_first_frame(frames):
    if frames[1].winfo_ismapped():
        frames[1].pack_forget()
    frames[0].pack()

def show_last_frame(frames):
    idx = len(frames) - 1
    if frames[idx - 1].winfo_ismapped():
        frames[idx - 1].pack_forget()
    frames[idx].pack()

def show_middle_frame(frames, i):
    if i == 0:
        show_first_frame(frames)
    elif i == len(frames) - 1:
        show_last_frame(frames)
    else:
        if frames[i - 1].winfo_ismapped():
            frames[i - 1].pack_forget()
        if frames[i + 1].winfo_ismapped():
            frames[i + 1].pack_forget()

    frames[i].pack()