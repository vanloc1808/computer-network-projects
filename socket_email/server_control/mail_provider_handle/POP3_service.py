import logging
import poplib
import threading
from queue import Queue
from time import sleep

from socket_email.server_control.mail_provider_handle.env import email, password

logging.basicConfig(format='%(asctime)s\n\t%(message)s', level=logging.INFO)

SERVER_NAME = 'outlook.office365.com'
PORT = 995

RELOAD_TIME = 10 # Reload cost 10 seconds

mail_queue = Queue(0) # Max queue

def get_mails():
    receiver = poplib.POP3_SSL(SERVER_NAME, PORT)
    receiver.getwelcome()
    receiver.user(email.decode())
    receiver.pass_(password.decode())
    logging.info("[?] Connected successfully!")


    num_mess = len(receiver.list()[1])
    for x in range(num_mess - 1, -1, -1): # from n - 1 to 0 to get newest -> oldest
        logging.info(f"Mail {x + 1} received!")
        sender = ""
        subject = ""

        ptr = 0

        ret = receiver.retr(x + 1)[1]

        for line in ret:
            if line[:5] == b'From:':
                sender = line[line.rfind(b'<') : -1]
            if line[:8] == b'Subject:':
                subject = line[9:]
            if line == b'Content-Type: text/plain; charset="UTF-8"':
                break
            ptr += 1

        content = b''
        for i in range(ptr + 2, len(ret)):
            if ret[i] == b'':
                break
            if content != b'':
                content += b' ' + ret[i]
            else:
                content = ret[i]

        # Mix
        if content != b'':
            subject += b' ' + content
        mail_queue.put((sender, subject))
        # delete that message:
        receiver.dele(x + 1)
    receiver.quit()
    logging.info("[?] Disconnected successfully!")

def loop():
    while True:
        get_mails()
        sleep(RELOAD_TIME)

t = threading.Thread(target=loop, args=())
t.start()