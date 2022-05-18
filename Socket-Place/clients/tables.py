import tkinter as tk
from functools import partial
from util import *

class Table(tk.LabelFrame):
    def __init__(self, received_data, column_headings, dictionary_headings, *args, **kwargs):
        tk.LabelFrame.__init__(self, *args, **kwargs)
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=6)
        self.grid_columnconfigure(2, weight=3)
        tk.Label(self, text=column_headings[0], anchor="center").grid(row=0, column=0, sticky="ew")
        tk.Label(self, text=column_headings[1], anchor="center").grid(row=0, column=1, sticky="ew")
        tk.Label(self, text=column_headings[2], anchor="center").grid(row=0, column=2, sticky="ew")

        row = 1
        for data in received_data:
            id = data[dictionary_headings[0]]
            name = data[dictionary_headings[1]]
            lbl_id = tk.Label(self, text=str(id), anchor='w')
            lbl_name = tk.Label(self, text=name, anchor='w')
            btn_detail = tk.Button(self, text='Xem chi tiết', command=partial(query_one_place_clicked, id, name))

            lbl_id.grid(row=row, column=0, sticky="w")
            lbl_name.grid(row=row, column=1, sticky="w")
            btn_detail.grid(row=row, column=2, sticky="w")

            row += 1