import tkinter as tk
from functools import partial

class Table(tk.LabelFrame):
    def __init__(self, received_data, *args, **kwargs):
        tk.LabelFrame.__init__(self, *args, **kwargs)
        self.grid_columnconfigure(1, weight=1)
        tk.Label(self, text="ID", anchor="w").grid(row=0, column=0, sticky="ew")
        tk.Label(self, text="Tên địa điểm", anchor="w").grid(row=0, column=1, sticky="ew")
        tk.Label(self, text="Chi tiết địa điểm", anchor="w").grid(row=0, column=2, sticky="ew")

        row = 1
        for data in received_data:
            id = data['ID']
            name = data['Name']
            lbl_id = tk.Label(self, text=str(id), anchor='w')
            lbl_name = tk.Label(self, text=name, anchor='w')
            btn_detail = tk.Button(self, text='Xem chi tiết', command=partial(self.query_one_places, id))

            lbl_id.grid(row=row, column=0, sticky="ew")
            lbl_name.grid(row=row, column=1, sticky="ew")
            btn_detail.grid(row=row, column=2, sticky="ew")

            row += 1

    def query_one_places(id):
        print('Hello')

def main():
    root = tk.Tk()
    data = [   {"ID": "BID", "Name": "Bình Dương"}, 
                    {"ID": "CDA", "Name": "Côn Đảo"}, 
                    {"ID": "DAN", "Name": "Đà Nẵng"}, 
                    {"ID": "HAN", "Name": "Hà Nội"}, 
                    {"ID": "NHT", "Name": "Nha Trang"}, 
                    {"ID": "TRV", "Name": "Trà Vinh"}, 
                    {"ID": "VTA", "Name": "Vũng Tàu"}   ]
    Table(data, root, text='Danh sách').pack(side="top", fill="both", expand=True, padx=10, pady=10)
    root.mainloop()

main()