# Socket
# import socket

# Work with Image
from PIL import ImageGrab
import io
import time

BUFSIZ = 4 * 1024

# Thread
# from threading import Thread


def capture_screen(client):
    INFO_SZ = 100
    time_to_rec = 0.5

    current = time.time()
    while time.time() - current < time_to_rec:
        # Capture screen
        img = ImageGrab.grab()
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes = img_bytes.getvalue()

        # Send image
        client.sendall(str(len(img_bytes)).ljust(INFO_SZ).encode())
        client.sendall(img_bytes)
    print("Ah finish")
    client.sendall(b'END'.ljust(BUFSIZ))