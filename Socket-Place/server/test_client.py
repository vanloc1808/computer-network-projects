# fileclient.py

import socket 

def recvall(sock):
    BUFF_SIZE = 4096 # 4 KiB
    data = b''
    while True:
        part = sock.recv(BUFF_SIZE)
        data += part
        if len(part) < BUFF_SIZE:
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

data = recvall(s)
f = open("a.jpg", 'wb')
f.write(data)
f.close()
# print(data)

s.close()
