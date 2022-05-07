import tkinter as tk

def close_event(main, client):
    client.sendall(bytes("QUIT", "utf8"))
    main.destroy()
    return

def shutdown(client):
    client.sendall(bytes("SHUTDOWN", "utf8"))
def logout(client):
    client.sendall(bytes("LOGOUT", "utf8"))

def shutdown_logout(client, root):
    window = tk.Toplevel(root)
    window.geometry("190x160")
    window.grab_set()
    window.protocol("WM_DELETE_WINDOW", lambda: close_event(window, client))
    shutdown_btn = tk.Button(window, text = 'SHUTDOWN', width = 20, height = 2, fg = 'white', bg = 'IndianRed3', command = lambda: shutdown(client), padx = 20, pady = 20)
    shutdown_btn.grid(row = 0, column = 0)
    logout_btn = tk.Button(window, text = 'LOGOUT', width = 20, height = 2, fg = 'white', bg = 'royalblue4', command = lambda: logout(client), padx = 20, pady = 20)
    logout_btn.grid(row = 1, column = 0)
    window.mainloop()
