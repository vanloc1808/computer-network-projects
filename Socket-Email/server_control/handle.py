import re

def is_valid_ip(ip):
    ip_address = "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
    port = "([0-9]|[1-9][0-9]|[1-9][0-9]{2}|[1-9][0-9]{3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])"
    ip_pattern = re.compile(r"^" + ip_address + "\\." + ip_address + "\\." + ip_address + "\\." + ip_address + "\\:" + port + "$")
    
    if (ip_pattern.match(ip)):
        return True
    
    return False

def raise_error_message(error_message):
    print(error_message)

def main():
    ip = "([0-9]|[1-9][0-9]|1[0-9][0-9]|2[0-4][0-9]|25[0-5])"
    port = "([0-9]|[1-9][0-9]|[1-9][0-9]{2}|[1-9][0-9]{3}|[1-5][0-9]{4}|6[0-4][0-9]{3}|65[0-4][0-9]{2}|655[0-2][0-9]|6553[0-5])"
    ip_pattern = re.compile(r"^" + ip + "\\." + ip + "\\." + ip + "\\." + ip + "\\:" + port + "$")

main()