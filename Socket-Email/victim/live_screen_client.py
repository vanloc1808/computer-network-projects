# Socket
import socket

# Work with Image
from PIL import ImageGrab
import io
import time

BUFSIZ = 4 * 1024

# Thread
from threading import Thread


def capture_screen(client):
    INFO_SZ = 100
    time_to_rec = 0.25

    current = time.time()
    while time.time() - current < time_to_rec:
        # Capture screen
        img = ImageGrab.grab()
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='JPEG')
        img_bytes = img_bytes.getvalue()

        # Send image
        client.sendall(str(len(img_bytes)).ljust(INFO_SZ).encode())
        client.sendall(img_bytes)
    print("Ah finish")
    client.sendall(b'END'.ljust(BUFSIZ))
    """
    img = ImageGrab.grab()
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    data = img_bytes.getvalue()
    
    # send frame size
    client.sendall(bytes(str(len(data)), "utf8"))

    # send frame data
    client.sendall(data)
    """

    """
    number_of_images = 100
    n = 1
    
    while (n <= number_of_images):
        img = ImageGrab.grab()
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        data = img_bytes.getvalue()
        
        # send frame size
        client.sendall(bytes(str(len(data)), "utf8"))

        # send frame data
        client.sendall(data)

        n += 1

        # listen to next command from client: continue or back

        check_stop = client.recv(INFO_SZ).decode("utf8")
        if("STOP_RECEIVING" in check_stop):
            break
    """


            



