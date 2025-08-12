"""Helper to display a MAC address returned from the server."""

import tkinter as tk

BUFSIZ = 1024 * 4


def mac_address(client):
    """Receive a raw hex MAC string from server and show it as AA:BB:..."""
    res = client.recv(BUFSIZ).decode("utf8")
    res = res[2:].upper()
    res = ":".join(res[i : i + 2] for i in range(0, len(res), 2))
    tk.messagebox.showinfo(title="MAC Address", message=res)
