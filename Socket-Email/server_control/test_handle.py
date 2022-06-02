from collections import defaultdict
from old_handle import app_process_client
from old_handle import directory_tree_client
from old_handle import keylogger_client
from old_handle import live_screen_client
from old_handle import mac_address_client
from old_handle import registry_client
from old_handle import shutdown_logout_client
from queue import Queue


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
        app_process_client._list(conn, "PROCESS") 
    )
    action_dictionary[ip_address].put(action_message)


def list_application(ip_address):
    action_message = lambda conn: app_process_client._list(conn, "APPLICATION")
    action_dictionary[ip_address].put(action_message)

def kill_process(ip_address, id):
    action_message = lambda conn: app_process_client.send_kill(conn, id)
    action_dictionary[ip_address].put(action_message)

def kill_application(ip_address, id):
    action_message = lambda conn: app_process_client.send_kill(conn, id)
    action_dictionary[ip_address].put(action_message)

def capture_webcam(ip_address, time):
    pass

def capture_screen(ip_address):
    pass

def shut_down(ip_address):
    action_message = lambda conn: shutdown_logout_client.shutdown(conn)
    action_dictionary[ip_address].put(action_message)

def logout(ip_address):
    action_message = lambda conn: shutdown_logout_client.logout(conn)
    action_dictionary[ip_address].put(action_message)

def restart(ip_address):
    action_message = lambda conn: app_process_client.restart(conn)
    action_dictionary[ip_address].put(action_message)

def mac_address(ip_address):
    action_message = lambda conn: mac_address_client.mac_address(conn)
    action_dictionary[ip_address].put(action_message)

def keylog(ip_address, time):
    pass

def registry_list(ip_address, path_to_folder):
    pass

def registry_update(ip_address, absolute_path, value):
    pass

def dir_list(ip_address, path_to_folder):
    action_message = lambda conn: directory_tree_client.dir_list(conn, path_to_folder)
    action_dictionary[ip_address].put(action_message)

def dir_copy(ip_address, src_path, dst_path):
    pass
