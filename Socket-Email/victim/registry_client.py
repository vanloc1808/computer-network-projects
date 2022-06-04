import re, winreg, json
import os

#from live_screen_client import BUFSIZ
BUFSIZ = 1024 * 4

import winreg
import registry_client as rc
import json

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
        except WindowsError as e:
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
        except WindowsError as e:
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
    except:
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
    except:
        return None, None, None

def query_value(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
        winreg.QueryValueEx(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except:
        return ["0", "0"]


def get_value(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_READ)
        value_of_value, value_type = winreg.QueryValueEx(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", value_of_value]
    except:
        return ["0", "0"]

def dec_value(c):
    c = c.upper()
    if ord('0') <= ord(c) and ord(c) <= ord('9'):
        return ord(c) - ord('0')
    if ord('A') <= ord(c) and ord(c) <= ord('F'):
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
    for i in range(0, len(s)):
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
    except:
        return ["0", "0"]


def delete_value(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1], 0, winreg.KEY_WRITE)
        winreg.DeleteValue(opened_key, value_list[2])
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except:
        return ["0", "0"]


def query_key(full_path):
    value_list = parse_data(full_path)
    try:
        opened_key = winreg.OpenKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2], 0, winreg.KEY_READ)
        winreg.CloseKey(opened_key)
        return ["1", "1"]
    except:
        return ["0", "0"]


def create_key(full_path):
    value_list = parse_data(full_path)
    try:
        winreg.CreateKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])
        return ["1", "1"]
    except:
        return ["0", "0"]


def delete_key(full_path):
    value_list = parse_data(full_path)
    try:
        winreg.DeleteKey(getattr(winreg, value_list[0]), value_list[1] + r'\\' + value_list[2])
        return ["1", "1"]
    except:
        return ["0", "0"]

def registry_handle(conn):
    BUFSIZ = 32768
    while True:
        msg = conn.recv(BUFSIZ).decode('utf8')
        if not msg:
            break
        if 'STOP' in msg:
            return
        if 'LIST' in msg:
            reg_dict = {}
            print(msg)
            full_path = msg.split(' ')[1]
            result = list_all_registry_entries(full_path, reg_dict)
            if (result == ["0", "0"]):
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
            if (result == ["0", "0"]):
                conn.send("FAIL".encode('utf8'))
            else:
                conn.send("OK".encode('utf8'))


def registry(client):
    BUFSIZ = 32768
    while True:
        header = client.recv(BUFSIZ).decode("utf8")
        if("STOP_EDIT_REGISTRY" in header):
            break
        data_sz = int(header)
        data = b""
        while len(data) < data_sz:
            packet = client.recv(BUFSIZ)
            data += packet

        msg = json.loads(data.decode('utf8'))
        # extract elements
        ID = msg['ID']
        full_path = msg['path'] 
        name_value = msg['name_value']
        value = msg['value']
        v_type = msg['v_type']
        res = ['0','0']

        print(ID)
        print(full_path)
        print(name_value)
        print(value)
        print(v_type)

        #ID==0 run file.reg
        #path is detail of file .reg
        if ID == 0:
            try:
                outout_file = os.getcwd() + '\\run.reg'
                with open(outout_file, 'w+') as f:
                    f.write(full_path)
                    f.close()
                os.system(r'regedit /s ' + os.getcwd() + '\\run.reg')
                res = ["1", "1"]
                print('file reg created')
            except:
                res = ["0", "0"]
                print('cannot create file reg')

        elif ID == 1:
            res = get_value(full_path + r'\\' + name_value)     

        elif ID == 2:
            res = set_value(full_path + r'\\' + name_value, value, v_type)       

        elif ID == 3:
            res = create_key(full_path)

        elif ID == 4:
            res = delete_key(full_path + r'\\')
        client.sendall(bytes(res[0], "utf8"))
        client.sendall(bytes(str(res[1]), "utf8"))

    return