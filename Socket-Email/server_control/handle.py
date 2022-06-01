import re

def is_valid_ip(ip):
    ip_address = "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
    port = "([0-9]|[1-9][0-9]|[1-9][0-9]{2}|[1-9][0-9]{3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])"
    ip_pattern = re.compile(r"^" + ip_address + "\\." + ip_address + "\\." + ip_address + "\\." + ip_address + "\\:" + port + "$")
    
    if (ip_pattern.match(ip)):
        return True
    
    return False

def authorize(sender_address, ip_address, ip_per_address):
    for d in ip_per_address:
        if sender_address in d:
            raise Exception("This email has already connected")
        
        if ip_address in d:
            raise Exception("This IP has already connected")
    
    ip_dict = {sender_address: ip_address}
    ip_per_address.append(ip_dict) 

def list_ip():
    pass

def list_process():
    pass

def list_application():
    pass

def kill_process(id):
    pass

def kill_application(id):
    pass

def capture_webcam(time):
    pass

def capture_screen():
    pass

def disconnect(sender_address, ip_per_address):
    connected = False
    for d in ip_per_address:
        if sender_address in d:
            ip_per_address.remove(d)
            connected = True
            break
    if connected == False:
        raise Exception("This email has not connected")

def shut_down():
    pass

def restart():
    pass

def keylog(time):
    pass

def registry_list(path_to_folder):
    pass

def registry_update(absolute_path, value):
    pass

def dir_list(path_to_folder):
    pass

def dir_copy(src_path, dst_path):
    pass

def raise_error_message(error_message):
    print(error_message)

def main():
    ip = "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
    port = "([0-9]|[1-9][0-9]|[1-9][0-9]{2}|[1-9][0-9]{3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])"
    ip_pattern = re.compile(r"^" + ip + "\\." + ip + "\\." + ip + "\\." + ip + "\\:" + port + "$")

main()