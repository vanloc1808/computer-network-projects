import tkinter as tk
import tkinter.ttk as ttk
from functools import partial
from util import *
from tables import *

def main():
    columns_headings = ['ID', 'Tên địa điểm', 'Chi tiết địa điểm']
    dictionary_headings = ['ID', 'Name']

    window = tk.Tk()

    data = [   {"ID": "BID", "Name": "Bình Dương"}, 
                    {"ID": "CDA", "Name": "Côn Đảo"}, 
                    {"ID": "DAN", "Name": "Đà Nẵng"}, 
                    {"ID": "HAN", "Name": "Hà Nội"}, 
                    {"ID": "NHT", "Name": "Nha Trang"}, 
                    {"ID": "TRV", "Name": "Trà Vinh"}, 
                    {"ID": "VTA", "Name": "Vũng Tàu"}   ]

    Table(data, columns_headings, dictionary_headings, window, text='Danh sách địa điểm').pack(side="top", fill="both", expand=True, padx=10, pady=10)

    window.mainloop()

if __name__ == "__main__":
    main()
