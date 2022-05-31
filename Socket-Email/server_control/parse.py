import socket as sk

import handle

"""
    AUTH <Key> <IP>: start connection to IP, return ACK
    LIST <Key>: list all connected IPs, return list str
    DISC: disconnect current connection, ACK
    double AUTH, error

    * PROCESS & ABP
        LIST_PROC (Name, PID, threads)
        LIST_ABP (Name, ID, threads)
        KILL <ID/PID>, ACK/Err
    
    * CAPTURING
        SCREENSHOT, a single image
        WEB/REC <seconds>, a video
        KEYLOG <seconds>, a list of actions
    
    * HIGHER PRIVILEGE COMMANDS
        SHUTDOWN/RESTART, ACK, call DISC afterwards
        REGISTRY, DIR:
            LIST <path to folder>, list of "directory/files"
            UPDATE <absolute path> <value>, ACK
        DIR COPY <src path> <dst path folder>, ACK
"""
def command_parser(message):
    msg = message.split(' ')
    file_in = open("keys.txt", "r")
    key = file_in.readline()
    key = key.strip()
    # print(key)
    file_in.close()

    try:
        if len(msg) > 4: # too many arguments
            raise Exception("Too many arguments")
        
        if len(msg) == 3:
            if (msg[0] != "AUTH"):
                raise Exception("Invalid command")
            
            if (msg[1] != key):
                raise Exception("Invalid key")
            
            if (handle.is_valid_ip(msg[2]) == False):
                raise Exception("Invalid IP")
            


    except Exception as e:
        handle.raise_error_message(e)      


def main():
    # msg = "Welcome to my heart aaa"
    # msg1 = "Hello I am"
    # msg2 = "AUTH 12439158102 3"
    # msg3 = "AUTH ABDCFE123465 2000.1"
    # command_parser(msg3)
    # command_parser(msg2)
    # x = msg.split(' ')
    # print(x)
    # print(type(x))
    # command_parser(msg)
    # command_parser(msg1)
    # msg = "AUTH ABDCFE123465 192.168.1.0:254"
    # command_parser(msg)
    # msg = "AUTH ABDCFE123465 255.255.255.255:65536"
    # command_parser(msg)
    print("End main")

main()