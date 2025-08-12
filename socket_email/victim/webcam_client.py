import socket
import time
from tempfile import gettempdir

import cv2

fourcc = cv2.VideoWriter_fourcc(*"XVID")
file_to_write = gettempdir() + "/" + "output.avi"

BUFSIZ = 4 * 1024


def send_file(conn: socket.socket):
    with open(file_to_write, "rb") as f:
        file = f.read()

    size = len(file)

    conn.sendall(str(size).encode().ljust(BUFSIZ))  # send length
    for idx in range(0, size, BUFSIZ):
        data_to_send = file[idx : idx + BUFSIZ]
        conn.sendall(data_to_send.ljust(BUFSIZ))  # prevent last block not aligned


def run(conn: socket.socket):
    msg = conn.recv(BUFSIZ).decode("utf8")
    try:
        time_to_rec = int(msg)
        # Record phase ----------------------------
        vc = cv2.VideoCapture(0)
        out = cv2.VideoWriter(file_to_write, fourcc, 24.0, (640, 480))

        if vc.isOpened():
            rval, frame = vc.read()
        else:
            rval = False

        if not rval:
            return

        current = time.time()
        while time.time() - current < time_to_rec:  # Lech ~2-5s do qua trinh chay
            out.write(frame)
            rval, frame = vc.read()

        vc.release()
        out.release()
        # End Record phase ------------------------
        send_file(conn)

    except Exception as e:
        print(e)
        pass
