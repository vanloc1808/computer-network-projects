import re
import winreg

BUFSIZ = 1024 * 4

def identify_hkey(value_list):
    if value_list[0] == 'HKEY_CURRENT_USER':
        return winreg.HKEY_CURRENT_USER
    elif value_list[0] == 'HKEY_LOCAL_MACHINE':
        return winreg.HKEY_LOCAL_MACHINE
    elif value_list[0] == 'HKEY_CLASSES_ROOT':
        return winreg.HKEY_CLASSES_ROOT
    elif value_list[0] == 'HKEY_USERS':
        return winreg.HKEY_USERS
    elif value_list[0] == 'HKEY_CURRENT_CONFIG':
        return winreg.HKEY_CURRENT_CONFIG
    else:
        return None

def get_value_of_key(key):
    key_dict = {}
    i = 0
    while True:
        try:
            subvalue = winreg.EnumValue(key, i)
        except OSError:
            break
        key_dict[subvalue[0]] = subvalue[1:]
        i+=1
    return key_dict


# https://stackoverflow.com/questions/32171448/python-winreg-get-key-values
def get_sub_keys(key):
    i = 0
    while True:
        try:
            subkey = winreg.EnumKey(key, i)
            yield subkey
            i += 1
        except OSError:
            break

def go_through_registry_tree(hkey, key_path, reg_dict):
    key = winreg.OpenKey(hkey, key_path, 0, winreg.KEY_READ)
    reg_dict[key_path] = get_value_of_key(key)

    for subkey in get_sub_keys(key):
        subkey_path = "%s\\%s" % (key_path, subkey)
        go_through_registry_tree(hkey, subkey_path, reg_dict)

def list_all_registry_entries(registry_path, reg_dict):
    # reg_dict = {}
    try:
        value_list = parse_data(registry_path)
        print(value_list)

        key_path = value_list[1] + '\\' + value_list[2]
        print(key_path)

        hkey = identify_hkey(value_list)
        go_through_registry_tree(hkey, key_path, reg_dict)
        return ["1", "1"]
    except Exception:
        return ["0", "0"]


def parse_data(full_path):
    try:
        full_path = re.sub(r'/', r'\\', full_path)
        hive = re.sub(r'\\.*$', '', full_path)
        if not hive:
            raise ValueError('Invalid \'full_path\' param.')
        if len(hive) <= 4:
            if hive == 'HKLM':
                hive = 'HKEY_LOCAL_MACHINE'
            elif hive == 'HKCU':
                hive = 'HKEY_CURRENT_USER'
            elif hive == 'HKCR':
                hive = 'HKEY_CLASSES_ROOT'
            elif hive == 'HKU':
                hive = 'HKEY_USERS'
        reg_key = re.sub(r'^[A-Z_]*\\', '', full_path)
        reg_key = re.sub(r'\\[^\\]+$', '', reg_key)
        reg_value = re.sub(r'^.*\\', '', full_path)
        return hive, reg_key, reg_value
    except Exception:
        return None, None, None

def dec_value(c):
    c = c.upper()
    if ord('0') <= ord(c) <= ord('9'):
        return ord(c) - ord('0')
    if ord('A') <= ord(c) <= ord('F'):
        return ord(c) - ord('A') + 10
    return 0

def str_to_bin(s):
    res = b""
    for i in range(0, len(s), 2):
        a = dec_value(s[i])
        b = dec_value(s[i + 1])
        res += (a * 16 + b).to_bytes(1, byteorder='big')
    return res

def str_to_dec(s):
    s = s.upper()
    res = 0
    for i in range(len(s)):
        v = dec_value(s[i])
        res = res*16 + v
    return res


def set_value(full_path, value, value_type):
    value_list = parse_data(full_path)
    try:
        winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1])
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
        if 'REG_BINARY' in value_type:
            if len(value) % 2 == 1:
                value += '0'
            value = str_to_bin(value)
        if 'REG_DWORD' in value_type:
            if len(value) > 8:
                value = value[:8]
            value = str_to_dec(value)
        if 'REG_QWORD' in value_type:
            if len(value) > 16:
                value = value[:16]
            value = str_to_dec(value)

        winreg.SetValueEx(opened_key, value_list[2], 0, getattr(winreg, value_type), value)
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except Exception:
        return ["0", "0"]

def registry_handle(conn):
    BUFSIZ = 32768
    msg = conn.recv(BUFSIZ).decode('utf8')
    if not msg:
        return
    if 'LIST' in msg:
        reg_dict = {}
        print(msg)
        full_path = msg.split(' ')[1]
        result = list_all_registry_entries(full_path, reg_dict)
        if result == ["0", "0"]:
            conn.send("FAIL")
        else:
            string_dictionary = str(reg_dict)
            conn.send(str(len(string_dictionary)).encode('utf8'))
            conn.send(string_dictionary.encode('utf8'))
    if 'UPDATE' in msg:
        full_path = msg.split(' ')[1]
        value = msg.split(' ')[2]
        value_type = msg.split(' ')[3]
        print(msg)
        result = set_value(full_path, value, value_type)
        if result == ["0", "0"]:
            conn.send("FAIL".encode('utf8'))
        else:
            conn.send("OK".encode('utf8'))