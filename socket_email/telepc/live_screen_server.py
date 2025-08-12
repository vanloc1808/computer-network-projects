"""Image capture loop for streaming the desktop to a connected client."""

# Socket

# Work with Image
import io

from PIL import ImageGrab

# Thread


def capture_screen(client):
    """Continuously capture the screen and send PNG frames over the socket."""
    INFO_SZ = 100
    while client:
        img = ImageGrab.grab()
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        data = img_bytes.getvalue()

        # send frame size
        client.sendall(bytes(str(len(data)), "utf8"))

        # send frame data
        client.sendall(data)

        # listen to next command from client: continue or back
        check_stop = client.recv(INFO_SZ).decode("utf8")
        if "STOP_RECEIVING" in check_stop:
            break
