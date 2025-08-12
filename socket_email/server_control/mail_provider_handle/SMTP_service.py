import smtplib
import threading
from time import sleep

from socket_email.server_control.mail_provider_handle.env import email, password

# https://www.tutorialspoint.com/send-mail-with-attachment-from-your-gmail-account-using-python
# https://www.codeforests.com/2020/06/22/how-to-send-email-via-python/
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
# from email import encoders

HOST = "smtp.office365.com"
PORT = 587

RELOAD_TIME = 10 # Reload cost 10 seconds

# content_ : bytes | str, must specify file_name if bytes
def send(to_: str, subject_: str, content_, file_name: str | None) -> None:
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
        # Default filename if not provided
        attachment_name = file_name or "attachment.bin"
        payload = MIMEApplication(content_)
        payload.add_header('Content-Disposition', f'attachment; filename={attachment_name}')
        message.attach(payload)

    text = message.as_string()
    sender.sendmail(email.decode(), to_, msg = text)

    sender.quit()

# adding exception handling
def safe_send(to_: str, subject_: str, content_, file_name: str | None) -> None:
    while True:
        try:
            send(to_, subject_, content_, file_name)
            print("MAIL SENT!")
            break
        except Exception:
            sleep(RELOAD_TIME)


# Modified to safer version
def send_threading(to_: str, subject_: str, content_, file_name: str | None = "x.txt") -> None:
    t = threading.Thread(target=safe_send, args=(to_, subject_, content_, file_name))
    t.start()
