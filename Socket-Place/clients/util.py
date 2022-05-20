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
    w['bg'] = '#F8FBF3'
    w.geometry('800x600')

    # details = query_one_place(id)
    
    details = get_detail_info(id)

    place_id = details['ID']
    place_name = details['Name']
    place_coordinate = details['Coordinate']
    place_description = details['Description']

    # frames and labels
    frm_id = tk.Frame(master=w, bg='#98C1D8')
    frm_id.pack(side='top', fill='x', padx=10, pady=10)
    lbl_id = tk.Label(master=frm_id, text='ID: ' + place_id, bg='#98C1D8', fg='red')
    lbl_id.pack(side='left', fill='x', padx=10, pady=10)

    frm_name = tk.Frame(master=w, bg='#98D8B2')
    frm_name.pack(side='top', fill='x', padx=10, pady=10)
    lbl_name = tk.Label(master=frm_name, text='Tên địa điểm: ' + place_name, bg='#98D8B2', fg='red')
    lbl_name.pack(side='left', fill='x', padx=10, pady=10)

    frm_coordinate = tk.Frame(master=w, bg='#D8AD98')
    frm_coordinate.pack(side='top', fill='x', padx=10, pady=10)
    str_coordinate = '(' + str(place_coordinate[0]) + ', ' + str(place_coordinate[1]) + ')'
    lbl_coordinate = tk.Label(master=frm_coordinate, text='Tọa độ: ' + str_coordinate, bg='#D8AD98', fg='red')
    lbl_coordinate.pack(side='left', fill='x', padx=10, pady=10)

    frm_description = tk.Frame(master=w, bg='#D8989C')
    frm_description.pack(side='top', fill='x', padx=10, pady=10)
    break_list = ['.', '!', '?']
    for i in range(len(place_description)):
        if (place_description[i] in break_list):
            new_des = place_description[:i + 1] + '\n' + place_description[i + 1:]
            place_description = new_des
    # print(place_description)
    lbl_description = tk.Label(master=frm_description, text='Mô tả: ' + place_description, bg='#D8989C', fg='red', anchor="w", justify=tk.LEFT)
    lbl_description.pack(side='left', fill='x', padx=10, pady=10, anchor='nw')

    frm_avatar = tk.Frame(master=w)
    frm_avatar.pack(side='top', fill='x', padx=10, pady=10)
    img_avatar = ImageTk.PhotoImage(Image.open(get_avt(id)).resize((200, 200), Image.ANTIALIAS))
    lbl_avatar = tk.Label(master=frm_avatar, image=img_avatar)
    lbl_avatar.image = img_avatar
    lbl_avatar.pack(side='bottom', fill='x', padx=10, pady=10)

    w.mainloop()

def download_images_one_place_clicked(id, name, images_num):
    w = tk.Toplevel()
    w.title('Hình ảnh từ ' + name)
    w.geometry('500x400')

    images_path = []
    for i in range(0, images_num - 1):
        images_path.append(get_img(id, i))
    # print(images_path)

    frames = []
    size = (400, 300)
    for i in range(0, images_num - 1):
        img = images_path[i]
        page = Page(id, name, img, size, w)
        frames.append(page)

    create_frames(frames)

    show_first_frame(frames)

    w.mainloop()

def download_all_avatars_clicked(id_list, name_list):
    w = tk.Toplevel()
    w.title('Hình đại diện các địa điểm')
    w.geometry('500x400')

    avatars_path = []
    for id in id_list:
        avatars_path.append(get_avt(id))
    # print(avatars_path)

    frames = []
    for i in range(len(id_list)):
        id = id_list[i]
        name = name_list[i]
        avt = avatars_path[i]
        size = (256, 256)
        page = Page(id, name, avt, size, w)
        frames.append(page)

    create_frames(frames)

    show_first_frame(frames)

    w.mainloop()