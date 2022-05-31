# Example on interractive server!

# Can use client's library to handle!

import socket as sk
import threading

HOST = '' # Localhost
PORT = 1337

list_of_ip = []

s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(4) # Upto 4 clients (4 threads)


def handle_thread(conn, addr):
    print("[?] Connection from ", addr)
    list_of_ip.append(addr)
    while True:
        inp = input().encode()
        print("Your input: ", inp)
        conn.sendall(inp)
        print("Recv: ", conn.recv(4096))
        if b"QUIT" in inp:
            break
    conn.close()
    list_of_ip.remove(addr)

for i in range(4):
    client, addr = s.accept()
    t = threading.Thread(target=handle_thread, args=(client, addr))
    t.daemon = True
    t.start()
