from queue import Queue
import test_handle as handler

# a list of dictionary, each of which has the type
# { email_address: IP connected }
ip_per_address = [] 

q = Queue(maxsize=0)

def get_corresponding_ip(sender_address):
    for i in ip_per_address:
        if i['email_address'] == sender_address:
            return i['IP']
    return None

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
            
        REGISTRY UPDATE <absolute path> <value> <data-type>, ACK
        DIR COPY <src path> <dst path folder>, ACK
"""
def command_parser(message, sender_address):
    msg = message.split(' ')
    file_in = open("keys.txt", "r")
    key = file_in.readline()
    key = key.strip()
    # print(key)
    file_in.close()

    try:
        if len(msg) > 5: # too many arguments
            raise Exception("Too many arguments")
        if len(msg) == 5:
             if msg[0] == "REGISTRY":
                if msg[1] == "UPDATE":
                    handler.registry_update(msg[2], msg[3], msg[4])
                else:
                    raise Exception("Invalid command")
        if len(msg) == 0:
            raise Exception("No arguments")
        
        if len(msg) == 4:
            if msg[0] == "DIR":
                if msg[1] == "COPY":
                    handler.dir_copy(msg[2], msg[3])
                else:
                    raise Exception("Invalid command")

            else:
                raise Exception("Invalid command")
        
        elif len(msg) == 3:
            if msg[0] == "AUTH":
                if msg[1] != key:
                   raise Exception("Invalid key")

                if handler.is_valid_ip(msg[2]) == False:
                    raise Exception("Invalid IP")  

                 # if the code goes here, it will start connection to the IP at msg[2]
                ip_address = msg[2]
                handler.authorize(sender_address, ip_address, ip_per_address)

            elif msg[0] == "REGISTRY":
                if msg[1] == "LIST":
                    handler.registry_list(msg[2])
                else:
                    raise Exception("Invalid command")

            elif msg[0] == "DIR":
                if msg[1] == "LIST":
                    handler.dir_list(msg[2])
                else:
                    raise Exception("Invalid command")

            else:
                raise Exception("Invalid command")

        elif len(msg) == 2:
            if msg[0] == "LIST":
                if msg[1] != key:
                    raise Exception("Invalid key")

                handler.list_ip()
            elif msg[0] == "KILL":
                list_of_process = handler.list_process()
                if msg[1] in list_of_process:
                    handler.kill_process(msg[1])
                else:
                    list_of_application = handler.list_application()
                    if msg[1] in list_of_application:
                        handler.kill_application(msg[1])
                    else:
                        raise Exception("Invalid PID or ID")
            elif msg[0] == "WEB" or msg[0] == "REC":
                if msg[1].isdigit() == False:
                    raise Exception("Invalid number of seconds")
                else:
                    handler.capture_webcam(int(msg[1]))
            elif msg[0] == "KEYLOG":
                if msg[1].isdigit() == False:
                    raise Exception("Invalid number of seconds")
                else:
                    handler.keylog(int(msg[1]))
            else:
                raise Exception("Invalid command")
        else:
            if msg[0] == "DISC": # disconnect 
                handler.disconnect(sender_address, ip_per_address)
            elif msg[0] == "LIST_PROC":
                handler.list_process()
            elif msg[0] == "LIST_ABP":
                handler.list_application()
            elif msg[0] == "SCREENSHOT":
                handler.capture_screen()
            elif msg[0] == "MAC":
                handler.mac_address()
            elif msg[0] == "SHUTDOWN":
                handler.shutdown()
                handler.disconnect(sender_address, ip_per_address)
            elif msg[0] == "LOGOUT":
                handler.logout()
                handler.disconnect(sender_address, ip_per_address)
            elif msg[0] == "RESTART":
                handler.restart()
                handler.disconnect(sender_address, ip_per_address)
            else:
                raise Exception("Invalid command")
                


    except Exception as e:
        handler.raise_error_message(e)      



def main():
    print("End main")

main()