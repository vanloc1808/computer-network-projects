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


def getSize(i, len_):
    return min(WINDOW_SIZE, len_ - i)

def getLen():
    while True:
        try:
            data, addr_port = UDP_cli.recvfrom(BLOCK_SIZE)
            if addr_port != (IP, PORT): continue # Not from server
            len_ = int(data.lstrip(b'\x00'))
            # Send back ACK:
            UDP_cli.sendto(f'ACK_LEN_{str(len_).rjust(3, "0")}'.encode().ljust(BLOCK_SIZE, b'\x00'), addr_port)
            return len_
        except sk.timeout:
            continue
        except ValueError:
            print("? Not a length")


def receiveData(len_):
    # Get length after send b'GIV':
    x = 0
    while x < len_:
        buffer = [None] * getSize(x, len_)
        while not all(buffer):
            for i in range(WINDOW_SIZE):
                if (x + i) >= len_: break
                if buffer[i] != None: continue
                
                d = UDP_cli.recvfrom(BLOCK_SIZE)
                
                id_ = int(d[0][:3])
                if (id_ < x): # Old packet
                    # Just send ACK back and do nothing!
                    print("? OLD ACK ", id_)
                    UDP_cli.sendto(f'ACK_{str(id_).rjust(3, "0")}'.encode().ljust(BLOCK_SIZE, b'\x00'), (IP, PORT))
                    continue

                print(d)
                buffer[i] = d
                # if randint(0, 1) == 0:
                #     print("[] LOSS :)")
                #     continue
                UDP_cli.sendto(f'ACK_{str(x + i).rjust(3, "0")}'.encode().ljust(BLOCK_SIZE, b'\x00'), (IP, PORT))
        x += WINDOW_SIZE

while True:
    mess = input()
    UDP_cli.sendto(mess.encode() + b'\n', (IP, PORT))
    if mess == 'GIV':
        l = getLen()
        print("[?] Len: ", l)
        receiveData(l)
        print("[?] DONE")