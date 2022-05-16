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
data_to_send = choices(vocab, k = BLOCK_SIZE * 5 + 123) # 5 + 1 block not rounded!
data_to_send = ''.join(data_to_send).encode()

sp = Spliter(BLOCK_SIZE)
block_list = sp.split_from_bytearray(data_to_send)
len_block_list = len(block_list)
print(len_block_list)
# Now send block_list to client when they requested!
# END testing: ---

cache = Queue(maxsize=0) # infinity queue

while True:
    mess, addr_port = UDP_sv.recvfrom(BLOCK_SIZE)
    print(f"[?] Receive message: {mess}")
    print(f"[?] From: {addr_port}")
    if mess == b'GIV\n':
        # Give block (USING SELECTIVE REPEAT)
        for i in range(0, len_block_list, WINDOW_SIZE):
            ack_list = [False] * min(WINDOW_SIZE, len_block_list - i)
            # Send phase
            while not all(ack_list):
                for j in range(len(ack_list)):
                    if not ack_list[j]: # Not sent / require resent
                        UDP_sv.sendto(block_list[i + j], addr_port)

                UDP_sv.settimeout(15) # 15 seconds to receive each ACK!
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
                        id_ = int(req[4:])
                        if (id_ - i < 0): continue # OLD packet!
                        ack_list[id_ - i] = True
                        print("[*] GOT ACK ", id_)
                    except sk.timeout: # Not received in time
                        continue
