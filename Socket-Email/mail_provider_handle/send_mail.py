import smtplib
from env import email, password
HOST = "smtp.office365.com"
PORT = 587

sender = smtplib.SMTP(HOST, PORT)
sender.starttls()
print(sender.login(email.decode(), password.decode()))
print(sender.quit())