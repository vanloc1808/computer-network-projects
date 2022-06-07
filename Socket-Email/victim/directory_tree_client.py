import pickle
import os
import shutil

#from directory_tree_client import BUFFER_SIZE
BUFFER_SIZE = 4096

BUFSIZ = 1024 * 4
SEPARATOR = "<SEPARATOR>" 

def directory_handle(conn):
    BUFSIZ = 32768 # caution!
    msg = conn.recv(BUFSIZ).decode('utf8')
    print(msg)
    if not msg:
        return
    if 'LIST' in msg:
        path_to_folder = msg.split(' ')[1]
        result = os.listdir(path_to_folder)
        print(result)
        conn.sendall(str(len(str(result))).encode('utf8'))
        # print(str(len(result)))
        conn.sendall(str(result).encode('utf8'))
    elif 'COPY' in msg:
        try:
            src_file = msg.split(' ')[1]
            dest = msg.split(' ')[2]
            shutil.copy(src_file, dest)
            conn.sendall('OK'.encode('utf8'))
        except:
            conn.sendall('ERROR'.encode('utf8'))