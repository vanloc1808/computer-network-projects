import tkinter as tk
import tkinter.ttk as ttk
from functools import partial
from util import *
from tables import *
from data import *

def main():
    columns_headings = ['ID', 'Tên địa điểm', 'Chi tiết địa điểm', '']
    dictionary_headings = ['ID', 'Name']

    window = tk.Tk()

    data = get_all_info()

    id_list = [d['ID'] for d in data]
    name_list = [d['Name'] for d in data]
    print(id_list)
    print(name_list)

    Table(data, columns_headings, dictionary_headings, window, text='Danh sách địa điểm').pack(side="top", fill="both", expand=True, padx=10, pady=10)

    frm_download_all_avt = tk.Frame(master=window)
    frm_download_all_avt.pack(side='top', fill='x', padx=10, pady=10)
    btn_download_all_avt = tk.Button(master=frm_download_all_avt, text='Tải tất cả hình ảnh đại diện', command=partial(download_all_avatars_clicked, id_list, name_list))
    btn_download_all_avt.pack(padx=10, pady=10)
    

    window.mainloop()

if __name__ == "__main__":
    main()
