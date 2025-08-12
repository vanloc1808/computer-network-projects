import logging
import socket as sk
from queue import Queue

from socket_place.common.config import BLOCK_SIZE, IP, PORT, WINDOW_SIZE
from socket_place.server import data_loader
from socket_place.server.spliter import Spliter

logging.basicConfig(
    format='%(asctime)s %(message)s', filename='program.log', level=logging.INFO
)

cache = Queue(maxsize=0) # infinity queue

# Init server host:
def init():
    sv = sk.socket(
        family  = sk.AF_INET,
        type    = sk.SOCK_DGRAM,
        proto   = sk.IPPROTO_UDP
    )
    sv.bind((IP, PORT))
    logging.info(f"[+] UDP server at {(IP, PORT)}")
    return sv

UDP_sv = init()

def getSize(idx, len_):
    return min(WINDOW_SIZE, len_ - idx)

def sendLen(addr_port, len_):
    done = False
    while not done:
        logging.info(f"[?] LEN: {len_}")
        UDP_sv.sendto(str(len_).encode().rjust(BLOCK_SIZE, b'\x00'), addr_port)
        UDP_sv.settimeout(1) # 1s timeout
        try:
            ack, r_addr = UDP_sv.recvfrom(BLOCK_SIZE)
            while r_addr != addr_port:
                cache.put((ack, r_addr))
                ack, r_addr = UDP_sv.recvfrom(BLOCK_SIZE)
            # request example: "ACK_LEN_000", send upto 999 blocks ~ 0.93mB real data
            if ack[:7] == b"ACK_LEN":  # Check packet
                if int(ack[8:11]) == len_:  # Check correct length
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
                if not ack_list[j]:  # Not sent / require resent
                    UDP_sv.sendto(data_to_send[i + j], addr_port)

            UDP_sv.settimeout(1)  # 1 seconds to receive each ACK!
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
                    id_ = int(req[4:7])
                    if id_ - i < 0:
                        # OLD packet!
                        continue
                    ack_list[id_ - i] = True
                    logging.info(f"[*] GOT ACK {id_}")
                except sk.timeout: # Not received in time
                    continue
            UDP_sv.settimeout(None)

data_loader.__init__()

sp = Spliter(BLOCK_SIZE)

def send(addr_port, s: bytearray) -> None:
    splited = sp.split_from_bytearray(s)
    sendLen(addr_port, len(splited))
    sendData(addr_port, splited)

while True:
    UDP_sv.settimeout(None)
    if cache.empty():
        mess, addr_port = UDP_sv.recvfrom(BLOCK_SIZE)
    else:
        mess, addr_port = cache.get()
    logging.info(f"[?] Receive message: {mess}")
    logging.info(f"[?] From: {addr_port}")

    # GIV_ALL
    if mess[:7] == b'GIV_ALL':
        logging.info(f"[?] Send all place to {addr_port}")
        send(addr_port, data_loader.query_all_places())
        continue
    # GIV_DETAIL_XXXX...
    if mess[:11] == b'GIV_DETAIL_':
        mess = mess.rstrip(b'\x00')
        id_ = mess[11:].decode('UTF-8')
        logging.info(f"[?] Send specific place({id_}) to {addr_port}")
        send(addr_port, data_loader.query_one_place(id_))
        continue
    # GIV_AVT_XXXX...
    if mess[:8] == b'GIV_AVT_':
        mess = mess.rstrip(b'\x00')
        id_ = mess[8:].decode('UTF-8')
        logging.info(f"[?] Send avatar of place({id_}) to {addr_port}")
        try:
            send(addr_port, data_loader.query_avatar(id_))
        except Exception:
            logging.error(f"[x] Not found {id_}")
        continue
    # GIV_IMG_YYY_XXXX...
    if mess[:8] == b'GIV_IMG_':
        mess = mess.rstrip(b'\x00')
        pos = int(mess[8:11]) # YYY
        id_ = mess[12:].decode('UTF-8') # XXXX...
        logging.info(f"[?] Send image place({id_}) number {pos + 1} to {addr_port}")
        try:
            send(addr_port, data_loader.query_image(id_, pos))
        except Exception:
            logging.error(f"[x] Not found {id_} or {pos} out of range!")
        continue
