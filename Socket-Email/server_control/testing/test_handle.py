from server_control import app_process_client
from server_control import directory_tree_client
from server_control import keylogger_client
from server_control import live_screen_client
from server_control import mac_address_client
from server_control import registry_client
from server_control import shutdown_logout_client
from queue import Queue

q = Queue(maxsize=0)

def list_ip():
    pass

def list_process(ip_address):
    message_to_ip = (ip_address, lambda conn, string: app_process_client.list_process(conn, string))
    q.put(message_to_ip)
    
    

def list_application(ip_address):
    pass

def kill_process(ip_address, id):
    pass

def kill_application(ip_address, id):
    pass

def capture_webcam(ip_address, time):
    pass

def capture_screen(ip_address):
    pass

def shut_down(ip_address):
    pass

def restart(ip_address):
    pass

def keylog(ip_address, time):
    pass

def registry_list(ip_address, path_to_folder):
    pass

def registry_update(ip_address, absolute_path, value):
    pass

def dir_list(ip_address, path_to_folder):
    pass

def dir_copy(ip_address, src_path, dst_path):
    pass
