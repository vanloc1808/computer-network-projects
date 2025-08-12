"""GUI client for interacting with the remote control server.

This module wires UI buttons to simple network commands, then delegates to
feature-specific UI components (live screen, registry editor, keylogger, etc.)
to handle interactions with the connected server.
"""

import socket
import tkinter as tk

from socket_email.telepc import app_process_client as ap
from socket_email.telepc import directory_tree_client as dt
from socket_email.telepc import entrance_ui as ui1
from socket_email.telepc import keylogger_client as kl
from socket_email.telepc import live_screen_client as lsc
from socket_email.telepc import mac_address_client as mac
from socket_email.telepc import main_ui as ui2
from socket_email.telepc import registry_client as rc
from socket_email.telepc import shutdown_logout_client as sl

# global variables
BUFSIZ = 1024 * 4
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
root = tk.Tk()
root.geometry("1000x600")
root.configure(bg="#FFFFFF")
root.title("Client")
root.resizable(False, False)
f1 = ui1.Entrance_UI(root)


def back(ui):
    """Return to the main menu from a child UI and notify the server."""
    ui.place_forget()
    f2.place(x=0, y=0)
    client.sendall(bytes("QUIT", "utf8"))


def live_screen():
    """Open the live screen UI and start the remote capture session."""
    client.sendall(bytes("LIVESCREEN", "utf8"))
    tmp = lsc.Desktop_UI(root, client)
    if not tmp.status:
        back(tmp)
    return


def shutdown_logout():
    """Open the shutdown/log out UI to perform power actions."""
    client.sendall(bytes("SD_LO", "utf8"))
    sl.shutdown_logout(client, root)
    return


def mac_address():
    """Request the remote host MAC address and display the result."""
    client.sendall(bytes("MAC", "utf8"))
    mac.mac_address(client)
    return


def back_dirTree(ui):
    """Return from the directory tree UI and end the sub-session."""
    ui.place_forget()
    ui.tree.pack_forget()
    f2.place(x=0, y=0)
    client.sendall(bytes("QUIT", "utf8"))


def directory_tree():
    """Open the directory tree UI to browse/copy/delete files."""
    client.sendall(bytes("DIRECTORY", "utf8"))
    tmp = dt.DirectoryTree_UI(root, client)
    tmp.button_6.configure(command=lambda: back_dirTree(tmp))
    return


def app_process():
    """Open the app/process UI for listing and terminating items."""
    client.sendall(bytes("APP_PRO", "utf8"))
    tmp = ap.App_Process_UI(root, client)
    tmp.button_6.configure(command=lambda: back(tmp))
    return


def disconnect():
    """Disconnect from the server and return to the connection screen."""
    f2.place_forget()
    f1.place(x=0, y=0)
    client.sendall(bytes("QUIT", "utf8"))
    return


def keylogger():
    """Open the keylogger UI and control capture/printing of keystrokes."""
    client.sendall(bytes("KEYLOG", "utf8"))
    tmp = kl.Keylogger_UI(root, client)
    tmp.button_6.configure(command=lambda: back(tmp))
    return


def registry():
    """Open the registry editor UI and begin a registry session."""
    client.sendall(bytes("REGISTRY", "utf8"))
    tmp = rc.Registry_UI(root, client)
    tmp.btn_back.configure(command=lambda: back_reg(tmp))
    return


def back_reg(ui):
    """Exit the registry UI, notify server to stop, and return to menu."""
    ui.client.sendall(bytes("STOP_EDIT_REGISTRY", "utf8"))
    ui.place_forget()
    f2.place(x=0, y=0)


def show_main_ui():
    """Instantiate and display the main menu UI with command bindings."""
    f1.place_forget()
    global f2
    f2 = ui2.Main_UI(root)
    f2.button_1.configure(command=live_screen)
    f2.button_2.configure(command=registry)
    f2.button_3.configure(command=mac_address)
    f2.button_4.configure(command=directory_tree)
    f2.button_5.configure(command=app_process)
    f2.button_6.configure(command=disconnect)
    f2.button_7.configure(command=keylogger)
    f2.button_8.configure(command=shutdown_logout)
    return


def connect():
    """Connect to the server using the IP from the entrance screen.

    Shows a success or error dialog and transitions to the main menu when
    connected.
    """
    global client
    ip = f1.input.get()
    try:
        client.connect((ip, 5656))
        tk.messagebox.showinfo(message="Connect successfully!")
        show_main_ui()
    except Exception:
        tk.messagebox.showerror(message="Cannot connect!")
    return


f1.button_1.configure(command=connect)
root.mainloop()
