import socket as sk
import threading
# from time import sleep

import test_parse as parser
import test_handle as handler

HOST = '' # Localhost
PORT = 1337

BUFSIZ = 1024 * 4

MAX_CONNECTION = 1

handler.conn_ip_list = []

s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(4) # Up to 4 clients (4 threads)

for i in range(MAX_CONNECTION):
    conn, addr = s.accept()
    handler.conn_ip_list.append((conn, addr))

handler.__init__()
print(handler.list_ip())


# Make connection with client
def _connect(conn, addr):
    print("[*] Connected to: ", addr)
    while True:
        # Blocking
        command_to_run = handler.action_dictionary[addr].get()
        command_to_run(conn)
        # conn.sendall(b'QUIT') # Quit current command
        break # For testing only 1 command
    conn.close()
    


# Sample authorize
def authorize(email, ip):
    if (email not in handler.auth_dict) or (not handler.auth_dict[email]):
        handler.auth_dict[email] = True
        handler.email_ip_dict[email] = ip

def check_return_ip(email):
    if email in handler.auth_dict and handler.auth_dict[email]:
        return handler.email_ip_dict[email]
    else:
        return None




# Sample connection (1 machine)
target = handler.conn_ip_list[0]

t = threading.Thread(target = _connect, args = target)
t.start()

# handler.list_process(target[1])
# handler.list_application(target[1])
# handler.kill_process(target[1], 20384)
# handler.kill_application(target[1], 12952)
# handler.keylog(target[1], 10)
# handler.shut_down(target[1])
# handler.logout(target[1])
# handler.restart(target[1])
# handler.mac_address(target[1])
# handler.capture_webcam(target[1], 10) # second
# handler.capture_screen(target[1], 10)
# handler.registry_list(target[1], "HKEY_LOCAL_MACHINE\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\2fcf99be")
# handler.registry_update(target[1], "HKEY_LOCAL_MACHINE\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\2fcf99be\\Hello", 'Hellooooooo_Worldddddd', 'REG_SZ')
# handler.dir_list(target[1], 'C:\\Users\\admin')
# handler.dir_copy(target[1], 'F:\\GitHub\\HCMUS-Computer-Networks-Projects\\Socket-Email\\victim\\requirements.txt', 'F:\\GitHub\\HCMUS-Computer-Networks-Projects\\Socket-Email')
email_address = 'vanloc1808@gmail.com'
parser.command_parser('LIST_PROC', email_address)