import smtplib
from env import email, password

import threading

# https://www.tutorialspoint.com/send-mail-with-attachment-from-your-gmail-account-using-python
# https://www.codeforests.com/2020/06/22/how-to-send-email-via-python/
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email import encoders

HOST = "smtp.office365.com"
PORT = 587

def send(to_:str, subject_:str, content_, file_name): # content_ : bytes | str, must specify file_name if bytes
    sender = smtplib.SMTP(HOST, PORT)
    sender.starttls()
    print(sender.login(email.decode(), password.decode()))

    message = MIMEMultipart()
    message["From"] = email.decode()
    message["To"] = to_
    message["Subject"] = subject_

    if isinstance(content_, str):
        message.attach(MIMEText(content_, 'plain'))
    else:
        payload = MIMEApplication(content_)
        payload.add_header('Content-Disposition', f'attachment; filename={file_name}')
        message.attach(payload)
    
    text = message.as_string()
    sender.sendmail(email.decode(), to_, msg = text)

    print(sender.quit())

def send_threading(to_:str, subject_:str, content_, file_name = "x.txt"):
    t = threading.Thread(target=send, args=(to_, subject_, content_, file_name))
    # t.setDaemon(True)
    t.start()

# Testing
TO = 'vanloc1808@gmail.com'
SUBJECT = 'NHAN DUOC THU CKUA ?'
# CONTENT = 'welcome to smtp world!'
CONTENT = open("./test.png", "rb").read()

send_threading(TO, SUBJECT, CONTENT, "test.png")