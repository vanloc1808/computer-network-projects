import socket as sk
from spliter import Spliter
from random import choices

from queue import Queue

from env import *

# Init server host:
def init():
    sv = sk.socket(
        family  = sk.AF_INET,
        type    = sk.SOCK_DGRAM,
        proto   = sk.IPPROTO_UDP
    )
    sv.bind((IP, PORT))
    print(f"[+] UDP server at {(IP, PORT)}")
    # sv.settimeout(1)
    return sv

# addr_cache = {} # IP -> Current action
UDP_sv = init()

# BEGIN testing: ----

vocab = "1234567890"
data_to_send = choices(vocab, k = BLOCK_SIZE * 3 + 123) # 3 + 1 block not rounded!
data_to_send = ''.join(data_to_send).encode()

sp = Spliter(BLOCK_SIZE)
block_list = sp.split_from_bytearray(data_to_send)
len_block_list = len(block_list)
print(len_block_list)
# Now send block_list to client when they requested!
# END testing: ---

cache = Queue(maxsize=0) # infinity queue

def getSize(idx, len_):
    return min(WINDOW_SIZE, len_ - idx)

def sendLen(addr_port, len_):
    done = False
    while not done:
        print(str(len_).encode().rjust(BLOCK_SIZE, b'\x00'))
        UDP_sv.sendto(str(len_).encode().rjust(BLOCK_SIZE, b'\x00'), addr_port)
        UDP_sv.settimeout(1) # 1s timeout
        try:
            ack, r_addr = UDP_sv.recvfrom(BLOCK_SIZE)
            while (r_addr != addr_port):
                cache.put((ack, r_addr))
                ack, r_addr = UDP_sv.recvfrom(BLOCK_SIZE)
            # request example: "ACK_LEN_000", send upto 999 blocks ~ 0.93gB real data
            if ack[:7] == b"ACK_LEN": # Check packet
                if int(ack[8:11]) == len_: # Check correct length
                    done = True
        except sk.timeout: # Not received in time
            continue
    UDP_sv.settimeout(None)

def sendData(addr_port, data_to_send):
    for i in range(0, len(data_to_send), WINDOW_SIZE):
        ack_list = [False] * getSize(i, len(data_to_send))
        # Send phase
        while not all(ack_list):
            for j in range(len(ack_list)):
                if not ack_list[j]: # Not sent / require resent
                    UDP_sv.sendto(data_to_send[i + j], addr_port)

            UDP_sv.settimeout(1) # 1 seconds to receive each ACK!
            for j in range(len(ack_list)):
                try:
                    req, req_addr = UDP_sv.recvfrom(BLOCK_SIZE)
                    while req_addr != addr_port:
                        # The data isn't from one we interacting!
                        # -> Move to queue (For later analyzing)
                        cache.put((req, req_addr))
                        # Retry
                        req, req_addr = UDP_sv.recvfrom(BLOCK_SIZE)
                    # Remember: only process 1 image at 1 time,
                    # if not, please revoke to end. It'll bug if 2 or more request
                    # of different data!

                    # request example: "ACK_000"
                    # print(req)
                    id_ = int(req[4:7])
                    # print(id_)
                    if (id_ - i < 0): continue # OLD packet!
                    ack_list[id_ - i] = True
                    print("[*] GOT ACK ", id_)
                except sk.timeout: # Not received in time
                    continue
            UDP_sv.settimeout(None)

print(UDP_sv.timeout)

while True:
    if cache.empty():
        mess, addr_port = UDP_sv.recvfrom(BLOCK_SIZE)
    else:
        mess, addr_port = cache.get()
    print(f"[?] Receive message: {mess}")
    print(f"[?] From: {addr_port}")
    if mess == b'GIV\n':
        # Give block (USING SELECTIVE REPEAT)
        sendLen(addr_port, len(block_list))
        sendData(addr_port, block_list)
