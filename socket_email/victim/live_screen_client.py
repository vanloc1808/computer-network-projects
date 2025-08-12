# Work with Image
import io
import time

from PIL import ImageGrab

BUFSIZ = 4 * 1024


def capture_screen(client):
    INFO_SZ = 100
    msg = client.recv(BUFSIZ).decode("utf8")
    print("Message: ", msg)
    try:
        time_to_rec = float(msg)
    except Exception:
        return

    current = time.time()
    while time.time() - current < time_to_rec:
        # Capture screen
        img = ImageGrab.grab()
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()

        # Send image
        client.sendall(str(len(img_bytes)).ljust(INFO_SZ).encode())
        client.sendall(img_bytes)
    print("finish")
    client.sendall(b"END".ljust(BUFSIZ))
