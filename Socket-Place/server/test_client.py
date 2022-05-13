# fileclient.py

import socket 

BLOCK_SIZE = 1024

def receive_all(sock):
    data = b''
    while True:
        part = sock.recv(BLOCK_SIZE)
        data += part
        if len(part) < BLOCK_SIZE:
            # either 0 or end of data
            break
    
    return data


s = socket.socket()
s.connect(("localhost", 6767)) #lắng nghe ở cổng 6767

#Nhập vào tên file 
filename = "images/TRV/avt.jpg"

#Gửi tên file cho server
s.send(filename.encode())

#Nhận được dữ liệu từ server gửi tới

data = receive_all(s)
print(data.decode('utf-8'))

s.close()
