import os

BUFSIZ = 1024 * 4
def shutdown_logout(msg):
    while(True):
        # msg = client.recv(BUFSIZ).decode("utf8")
        if "SHUTDOWN" in msg:
            os.system('shutdown -s -t 30')
        elif "LOGOUT" in msg:
            os.system('shutdown -l -t 30')
        elif "RESTART" in msg:
            os.system("shutdown -t 30 -r -f")
        else:
            return
    return
    