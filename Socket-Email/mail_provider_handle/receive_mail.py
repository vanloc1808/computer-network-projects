import poplib

from numpy import empty

from env import email, password
import logging
from time import sleep

from queue import Queue
import threading

logging.basicConfig(format='%(asctime)s\n\t%(message)s', level = logging.INFO)

SERVER_NAME = 'outlook.office365.com'
PORT = 995

RELOAD_TIME = 10 # Reload cost 10 seconds

q = Queue(0) # Max queue

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
        for line in receiver.retr(x + 1)[1]:
            if (line[:5] == b'From:'):
                sender = line[line.rfind(b'<') : -1]
            if (line[:8] == b'Subject:'):
                subject = line[9:]
                break
        q.put((sender, subject))
        # delete that message:
        receiver.dele(x + 1)
    receiver.quit()
    logging.info("[?] Disconnected successfully!")

def loop():
    while True:
        get_mails()
        sleep(RELOAD_TIME)

t = threading.Thread(target = loop, args=())
t.setDaemon(True)
t.start()

# Getting message prototype <>: q.get() -> (sender_mail, subject), can be use to pass to function
while True:
    while(not q.empty()):
        print("<get from queue>")
        print(q.get())
        q.task_done() # Required after get