import tkinter as tk
from PIL import ImageTk, Image
from functools import partial

class Page(tk.Frame):
    def __init__(self, id, name, avt, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        load_avt = Image.open(avt)
        load_avt = load_avt.resize((256, 256), Image.ANTIALIAS)
        photo_avt = ImageTk.PhotoImage(load_avt)

        lbl_avt = tk.Label(master=self, image=photo_avt)
        lbl_avt.image = photo_avt
        lbl_avt.pack()

        lbl_caption = tk.Label(master=self, text=name)
        lbl_caption.pack()

def create_first_frame(frames):
    frm_button = tk.Frame(master=frames[0])
    frm_button.pack(side='bottom')

    btn_next = tk.Button(master=frm_button, text='Next', command=partial(show_middle_frame, frames, 1))
    btn_next.pack(pady=30, side='right')

def create_last_frame(frames):
    idx = len(frames) - 1
    
    frm_buttons = tk.Frame(master=frames[idx])
    frm_buttons.pack(side='bottom')
    btn_next = tk.Button(master=frm_buttons, text='Prev', command=partial(show_middle_frame, frames, idx - 1))
    btn_next.pack(pady=30, side='left')

def create_middle_frames(frames, i):
    frm_buttons = tk.Frame(master=frames[i])
    frm_buttons.pack(side='bottom')
    btn_next = tk.Button(master=frm_buttons, text='Prev', command=partial(show_middle_frame, frames, i - 1))
    btn_next.pack(pady=30, side='left')
    btn_prev = tk.Button(master=frm_buttons, text='Next', command=partial(show_middle_frame, frames, i + 1))
    btn_prev.pack(pady=30, side='right')

def create_frames(frames):
    create_first_frame(frames)
    create_last_frame(frames)

    for i in range(1, len(frames) - 1, 1):
        create_middle_frames(frames, i)  

def show_first_frame(frames):
    if (frames[1].winfo_ismapped() == True):
        frames[1].destroy()
    frames[0].pack()     

def show_last_frame(frames):
    idx = len(frames) - 1
    if (frames[idx - 1].winfo_ismapped() == True):
        frames[idx - 1].destroy()
    frames[idx].pack()

def show_middle_frame(frames, i):
    if i == 0:
        show_first_frame(frames)
    elif i == len(frames) - 1:
        show_last_frame(frames)
    else:
        if (frames[i - 1].winfo_ismapped() == True):
            frames[i - 1].destroy()
        if (frames[i + 1].winfo_ismapped() == True):
            frames[i + 1].destroy()
    
    frames[i].pack()

root = tk.Tk()
id_list = ['BID', 'CDA', 'DAN', 'HAN', 'NHT', 'TRV', 'VTA']
name_list = ['Bình Dương', 'Côn Đảo', 'Đà Nẵng', 'Hà Nội', 'Nha Trang', 'Trà Vinh', 'Vũng Tàu']
avt_list = ['C:\\Users\\admin\\AppData\\Local\\Temp/facxfdfjbdfu.jpg', 'C:\\Users\\admin\\AppData\\Local\\Temp/bbopslevfhfs.jpg', 'C:\\Users\\admin\\AppData\\Local\\Temp/wnxdjmodcjns.jpg', 'C:\\Users\\admin\\AppData\\Local\\Temp/ipaayetkpvdi.jpg', 'C:\\Users\\admin\\AppData\\Local\\Temp/kicofdjszzbe.jpg', 'C:\\Users\\admin\\AppData\\Local\\Temp/owoaxwgdxajp.jpg', 'C:\\Users\\admin\\AppData\\Local\\Temp/tkeikijrdetq.jpg']

frames = []
for i in range(len(id_list)):
    id = id_list[i]
    name = name_list[i]
    avt = avt_list[i]

    page = Page(id, name, avt, root)
    frames.append(page)

create_frames(frames)

show_first_frame(frames)

root.mainloop()
