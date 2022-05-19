import tkinter as tk
import tkinter.ttk as ttk
from functools import partial
from PIL import ImageTk, Image
from data import *
from pages import *

# RGB link: https://htmlcolorcodes.com/

# FUNCTIONS FOR HANDLING MOUSE CLICK EVENTS
def query_one_place_clicked(id, name):
    w = tk.Toplevel()
    w.title("Chi tiết về " + name)
    w['bg'] = '#EAF40D'

    # details = query_one_place(id)
    
    details = get_detail_info(id)

    place_id = details['ID']
    place_name = details['Name']
    place_coordinate = details['Coordinate']
    place_description = details['Description']

    # frames and labels
    frm_id = tk.Frame(master=w, bg='#45F40D')
    frm_id.pack(side='top', fill='x', padx=10, pady=10)
    lbl_id = tk.Label(master=frm_id, text='ID: ' + place_id, bg='#45F40D', fg='red')
    lbl_id.pack(side='left', fill='x', padx=10, pady=10)

    frm_name = tk.Frame(master=w, bg='#0DE2F4')
    frm_name.pack(side='top', fill='x', padx=10, pady=10)
    lbl_name = tk.Label(master=frm_name, text='Tên địa điểm: ' + place_name, bg='#0DE2F4', fg='red')
    lbl_name.pack(side='left', fill='x', padx=10, pady=10)

    frm_coordinate = tk.Frame(master=w, bg='#0DC0F4')
    frm_coordinate.pack(side='top', fill='x', padx=10, pady=10)
    str_coordinate = '(' + str(place_coordinate[0]) + ', ' + str(place_coordinate[1]) + ')'
    lbl_coordinate = tk.Label(master=frm_coordinate, text='Tọa độ: ' + str_coordinate, bg='#0DC0F4', fg='red')
    lbl_coordinate.pack(side='left', fill='x', padx=10, pady=10)

    frm_description = tk.Frame(master=w, bg='#0DF468')
    frm_description.pack(side='top', fill='x', padx=10, pady=10)
    lbl_description = tk.Label(master=frm_description, text='Mô tả: ' + place_description, bg='#0DF468', fg='red')
    lbl_description.pack(side='left', fill='x', padx=10, pady=10)

    w.mainloop()

def download_images_one_place_clicked(id, name, images_num):
    w = tk.Toplevel()
    w.title('Hình ảnh từ ' + name)

    images_path = []
    for i in range(0, images_num - 1):
        images_path.append(get_img(id, i))
    print(images_path)

    frames = []
    for i in range(0, images_num - 1):
        img = images_path[i]
        page = Page(id, name, img , w)
        frames.append(page)

    create_frames(frames)

    show_first_frame(frames)

    w.mainloop()

def download_all_avatars_clicked(id_list, name_list):
    w = tk.Toplevel()
    w.title('Hình đại diện các địa điểm')


    avatars_path = []
    for id in id_list:
        avatars_path.append(get_avt(id))
    print(avatars_path)

    frames = []
    for i in range(len(id_list)):
        id = id_list[i]
        name = name_list[i]
        avt = avatars_path[i]

        page = Page(id, name, avt, w)
        frames.append(page)

    create_frames(frames)

    show_first_frame(frames)

    w.mainloop()