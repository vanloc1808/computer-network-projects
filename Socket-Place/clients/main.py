import socket as sk
from env import *

def init():
    sv = sk.socket(
        family  = sk.AF_INET,
        type    = sk.SOCK_DGRAM,
        proto   = sk.IPPROTO_UDP
    )
    # sv.bind((IP, PORT))
    # print(f"[+] UDP server at {(IP, PORT)}")
    return sv

UDP_cli = init()
#while True:
mess = input()
UDP_cli.sendto(mess.encode() + b'\n', (IP, PORT))
x = 0
while x < 22:
    for i in range(WINDOW_SIZE):
        if (x + i) >= 22: break
        d = UDP_cli.recvfrom(BLOCK_SIZE)
        UDP_cli.sendto(f'ACK_{str(x + i).rjust(3, "0")}'.encode(), (IP, PORT))
        print(d)
    x += WINDOW_SIZE