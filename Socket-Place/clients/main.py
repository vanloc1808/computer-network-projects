import tkinter as tk
from functools import partial
from PIL import Image, ImageTk

from util import download_all_avatars_clicked
from tables import Table
from data import get_all_info

def main():
    columns_headings = ['ID', 'Tên địa điểm', 'Chi tiết địa điểm', '']
    dictionary_headings = ['ID', 'Name', 'NOI']

    window = tk.Tk()
    window.title('Favorite Place')
    window.geometry('800x600')
    ico = Image.open('icon.jpg')
    photo = ImageTk.PhotoImage(ico)
    window.wm_iconphoto(False, photo)

    data = get_all_info()

    id_list = [d['ID'] for d in data]
    name_list = [d['Name'] for d in data]
    # number_of_images = [d['NOI'] for d in data]
    """
    print(id_list)
    print(name_list)
    print(number_of_images)
    """

    Table(data, columns_headings, dictionary_headings, window, text='Danh sách địa điểm').pack(side="top", fill="both", expand=True, padx=10, pady=10)

    frm_download_all_avt = tk.Frame(master=window)
    frm_download_all_avt.pack(side='top', fill='x', padx=10, pady=10)
    btn_download_all_avt = tk.Button(master=frm_download_all_avt, text='Tải tất cả hình ảnh đại diện', command=partial(download_all_avatars_clicked, id_list, name_list))
    btn_download_all_avt.pack(padx=10, pady=10)


    window.mainloop()

if __name__ == "__main__":
    main()
