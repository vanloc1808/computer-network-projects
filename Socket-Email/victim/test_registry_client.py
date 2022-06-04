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

def list_all_registry_entries(registry_path):
    reg_dict = {}
    value_list = rc.parse_data(registry_path)
    print(value_list)

    key_path = value_list[1] + '\\' + value_list[2]
    print(key_path)

    hkey = identify_hkey(value_list)
    go_through_registry_tree(hkey, key_path, reg_dict)
    return reg_dict



registry_path = "HKEY_LOCAL_MACHINE\\SOFTWARE\\Wow6432Node\\Microsoft\\Windows\\CurrentVersion\\Uninstall\\2fcf99be"
"""
reg_dict = list_all_registry_entries(registry_path)
out_file = open('dictionary.txt', 'wb')
for i in reg_dict:
    #print(i)
    out_file.write(i.encode('utf-8'))
    #out_file.write(b'\n')
    out_file.write(json.dumps(reg_dict[i]).encode('utf-8'))
    out_file.write(b'\n')


result = rc.get_value(registry_path + '\\2fcf99be' + "\\DisplayName")
result_update = rc.set_value(registry_path + '\\2fcf99be' + "\\DisplayName", "test", 'REG_SZ')
print(result)
print(result_update)
"""
# result = rc.get_value(registry_path)
# print(result)
# result_update = rc.set_value(registry_path, 'Visual Studio Community 2019', 'REG_SZ')
# print(result_update)
        
