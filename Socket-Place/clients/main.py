import socket as sk
from env import *

from random import randint

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

def getSize(i):
    return min(WINDOW_SIZE, 22 - x)

while x < 22:
    buffer = [None] * getSize(x)
    while not all(buffer):
        for i in range(WINDOW_SIZE):
            if (x + i) >= 22: break
            if buffer[i] != None: continue
            d = UDP_cli.recvfrom(BLOCK_SIZE)
            if randint(0, 1) == 0:
                print("[] LOSS :)")
                continue
            UDP_cli.sendto(f'ACK_{str(x + i).rjust(3, "0")}'.encode().ljust(BLOCK_SIZE, '\x00'), (IP, PORT))
            print(d)
            buffer[i] = d
    x += WINDOW_SIZE