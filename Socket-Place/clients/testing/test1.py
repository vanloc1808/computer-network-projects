def my_command():
    print("Test")

def create_first_page(pages):
    if (pages[1].winfo_ismapped() == True):
        pages[1].destroy()
    frm_buttons = tk.Frame(master=pages[0])
    frm_buttons.pack(side='bottom')
    btn_next = tk.Button(master=frm_buttons, text='Next', command=partial(show_middle_page, pages, 1))
    btn_next.pack(pady=30, side='right')
    pages[0].pack()

def show_last_page(pages):
    idx = len(pages) - 1
    if (pages[idx - 1].winfo_ismapped() == True):
        pages[idx - 1].destroy()

    frm_buttons = tk.Frame(master=pages[idx])
    frm_buttons.pack(side='bottom')
    btn_next = tk.Button(master=frm_buttons, text='Prev', command=partial(show_middle_page, pages, idx - 1))
    btn_next.pack(pady=30, side='left')
    pages[idx].pack()

def show_middle_page(pages, i):
    if i == 0:
        show_first_page(pages)
    elif i == len(pages) - 1:
        show_last_page(pages)
    else:
        """
        if (pages[i - 1].winfo_ismapped() == True):
            pages[i - 1].destroy()
        if (pages[i + 1].winfo_ismapped() == True):
            pages[i + 1].destroy()
        """
        frm_buttons = tk.Frame(master=pages[i])
        frm_buttons.pack(side='bottom')
        btn_next = tk.Button(master=frm_buttons, text='Prev', command=partial(show_middle_page, pages, i - 1))
        btn_next.pack(pady=30, side='left')
        btn_prev = tk.Button(master=frm_buttons, text='Next', command=partial(show_middle_page, pages, i + 1))
        btn_prev.pack(pady=30, side='right')
        pages[i].pack()

frames = []
for i in range(len(id_list)):
    id = id_list[i]
    name = name_list[i]
    avt = avt_list[i]

    page = Page(id, name, avt, root)
    frames.append(page)

show_first_page(frames)
# show_last_page(frames)