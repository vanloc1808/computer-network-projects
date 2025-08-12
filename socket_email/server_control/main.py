"""Main control server accepting client sockets and executing email commands."""

import socket as sk
from threading import Thread

import mail_parser

from socket_email.server_control.mail_provider_handle import POP3_service as p3

HOST = ""  # Localhost
PORT = 1337

BUFSIZ = 1024 * 4

MAX_CONNECTION = 2
mail_parser.handler.conn_ip_list = []

s = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
s.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(4)  # Up to 4 clients (4 threads)

print("SERVER STARTED")

# Warning: all client must connect before starting receive commands
for _ in range(MAX_CONNECTION):
    conn, addr = s.accept()
    mail_parser.handler.conn_ip_list.append((conn, addr))

mail_parser.handler.__init__()


def _connect(conn, addr):
    """Worker thread: execute queued actions for a given client connection."""
    print("[*] Connected to: ", addr)
    while True:
        # Blocking
        command_to_run = mail_parser.handler.action_dictionary[addr].get()
        command_to_run(conn)
    conn.close()


for i in range(MAX_CONNECTION):
    t = Thread(target=_connect, args=mail_parser.handler.conn_ip_list[i])
    t.start()

# Main loop:
while True:
    # Wait for new mail:
    sender, subject = p3.mail_queue.get()
    mail_parser.command_parser(subject.decode(), sender.decode())
