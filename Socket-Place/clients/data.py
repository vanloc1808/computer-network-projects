import socket as sk
from random import choices
from string import ascii_lowercase
from tempfile import gettempdir

from env import BLOCK_SIZE, IP, PORT, WINDOW_SIZE
from error_check import check_split_not_corrupted
from joiner import join

import logging
import json

logging.basicConfig(
    format='%(asctime)s %(message)s', filename='program.log', level=logging.INFO
)


def init():
    sv = sk.socket(
        family  = sk.AF_INET,
        type    = sk.SOCK_DGRAM,
        proto   = sk.IPPROTO_UDP
    )
    return sv

UDP_cli = init()
logging.info("[?] Client started!")

def getSize(i, len_):
    return min(WINDOW_SIZE, len_ - i)

def getLen():
    while True:
        try:
            data, addr_port = UDP_cli.recvfrom(BLOCK_SIZE)
            if addr_port != (IP, PORT):
                # Not from server
                continue
            len_ = int(data.lstrip(b'\x00'))
            # Send back ACK:
            UDP_cli.sendto(
                f'ACK_LEN_{str(len_).rjust(3, "0")}'.encode().ljust(BLOCK_SIZE, b'\x00'),
                addr_port,
            )
            return len_
        except sk.timeout:
            continue
        except ValueError:
            print("? Not a length")

def receiveData(len_):
    result = []
    x = 0
    while x < len_:
        buffer = [None] * getSize(x, len_)
        while not all(buffer):
            for i in range(WINDOW_SIZE):
                if (x + i) >= len_:
                    break
                if buffer[i] is not None:
                    continue

                d, addr_port = UDP_cli.recvfrom(BLOCK_SIZE)
                if addr_port != (IP, PORT):
                    # Not from server
                    continue

                id_ = int(d[:3])
                if (id_ < x): # Old packet
                    # Just send ACK back and do nothing!
                    logging.info(f"? OLD ACK {id_}")
                    UDP_cli.sendto(
                        f'ACK_{str(id_).rjust(3, "0")}'.encode().ljust(BLOCK_SIZE, b'\x00'),
                        (IP, PORT),
                    )
                    continue

                logging.info(f"Get: {d}")
                if not check_split_not_corrupted(d):
                    logging.warning("Corrupt datagram!")
                    # Skip
                    continue
                buffer[i] = d

                UDP_cli.sendto(
                    f'ACK_{str(x + i).rjust(3, "0")}'.encode().ljust(BLOCK_SIZE, b'\x00'),
                    (IP, PORT),
                )
            result = result + buffer
        x += WINDOW_SIZE
    result = sorted(result)
    return join(result)

def recvData():
    total_len = getLen()
    logging.info(f"[?] Len: {total_len}")
    received_data = receiveData(total_len)
    logging.info("[?] DONE")
    return received_data

def sendCommand(cmd):
    UDP_cli.sendto(cmd.ljust(BLOCK_SIZE, b'\x00'), (IP, PORT))

def get_all_info():
    sendCommand(b'GIV_ALL')
    d = recvData()
    return json.loads(d.rstrip(b'\x00'))

def get_detail_info(id_):
    sendCommand(f'GIV_DETAIL_{id_}'.encode())
    d = recvData()
    return json.loads(d.rstrip(b'\x00'))

def get_avt(id_):
    sendCommand(f'GIV_AVT_{id_}'.encode())
    d = recvData()
    # abcdefghijkl.jpg
    file_name = ''.join(choices(ascii_lowercase, k=12)) + '.jpg'
    path = gettempdir() + '/' + file_name
    x = open(path, 'wb')
    x.write(d)
    x.close()
    return path

def get_img(id_, pos):
    sendCommand(f'GIV_IMG_{str(pos).rjust(3, "0")}_{id_}'.encode())
    d = recvData()
    # abcdefghijkl.jpg
    file_name = ''.join(choices(ascii_lowercase, k=12)) + '.jpg'
    path = gettempdir() + '/' + file_name
    x = open(path, 'wb')
    x.write(d)
    x.close()
    return path


# while True:
#     mess = input()
#     UDP_cli.sendto(mess.encode(), (IP, PORT))
#     if mess[:3] == 'GIV':

#         x = open("tmp", "wb")
#         x.write(g)
#         x.close()