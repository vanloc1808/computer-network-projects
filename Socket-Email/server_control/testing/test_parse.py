from queue import Queue
import test_handle

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
            UPDATE <absolute path> <value>, ACK
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
        if len(msg) > 4: # too many arguments
            raise Exception("Too many arguments")
        if len(msg) == 0:
            raise Exception("No arguments")
        
        if len(msg) == 4:
            if msg[0] == "REGISTRY":
                if msg[1] == "UPDATE":
                    test_handle.registry_update(msg[2], msg[3])
                else:
                    raise Exception("Invalid command")

            elif msg[0] == "DIR":
                if msg[1] == "UPDATE":
                    test_handle.registry_update(msg[2], msg[3])
                elif msg[1] == "COPY":
                    test_handle.dir_copy(msg[2], msg[3])
                else:
                    raise Exception("Invalid command")

            else:
                raise Exception("Invalid command")
        
        elif len(msg) == 3:
            if msg[0] == "AUTH":
                if msg[1] != key:
                   raise Exception("Invalid key")

                if test_handle.is_valid_ip(msg[2]) == False:
                    raise Exception("Invalid IP")  

                 # if the code goes here, it will start connection to the IP at msg[2]
                ip_address = msg[2]
                test_handle.authorize(sender_address, ip_address, ip_per_address)

            elif msg[0] == "REGISTRY":
                if msg[1] == "LIST":
                    test_handle.registry_list(msg[2])
                else:
                    raise Exception("Invalid command")

            elif msg[0] == "DIR":
                if msg[1] == "LIST":
                    test_handle.dir_list(msg[2])
                else:
                    raise Exception("Invalid command")

            else:
                raise Exception("Invalid command")

        elif len(msg) == 2:
            if msg[0] == "LIST":
                if msg[1] != key:
                    raise Exception("Invalid key")

                test_handle.list_ip()
            elif msg[0] == "KILL":
                list_of_process = test_handle.list_process()
                if msg[1] in list_of_process:
                    test_handle.kill_process(msg[1])
                else:
                    list_of_application = test_handle.list_application()
                    if msg[1] in list_of_application:
                        test_handle.kill_application(msg[1])
                    else:
                        raise Exception("Invalid PID or ID")
            elif msg[0] == "WEB" or msg[0] == "REC":
                if msg[1].isdigit() == False:
                    raise Exception("Invalid number of seconds")
                else:
                    test_handle.capture_webcam(int(msg[1]))
            elif msg[0] == "KEYLOG":
                if msg[1].isdigit() == False:
                    raise Exception("Invalid number of seconds")
                else:
                    test_handle.keylog(int(msg[1]))
            else:
                raise Exception("Invalid command")
        else:
            if msg[0] == "DISC": # disconnect 
                test_handle.disconnect(sender_address, ip_per_address)
            elif msg[0] == "LIST_PROC":
                test_handle.list_process()
            elif msg[0] == "LIST_ABP":
                test_handle.list_application()
            elif msg[0] == "SCREENSHOT":
                test_handle.capture_screen()
            elif msg[0] == "MAC":
                test_handle.mac_address()
            elif msg[0] == "SHUTDOWN":
                test_handle.shutdown()
                test_handle.disconnect(sender_address, ip_per_address)
            elif msg[0] == "LOGOUT":
                test_handle.logout()
                test_handle.disconnect(sender_address, ip_per_address)
            elif msg[0] == "RESTART":
                test_handle.restart()
                test_handle.disconnect(sender_address, ip_per_address)
            else:
                raise Exception("Invalid command")
                


    except Exception as e:
        test_handle.raise_error_message(e)      


def main():
    print("End main")

main()