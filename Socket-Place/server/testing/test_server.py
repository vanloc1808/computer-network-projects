# fileserver.py

import socket 

host = 'localhost'
port = 6767

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
print("Server listening on port", port)

c, addr = s.accept()

#Nhận tên file do client gửi tới
filename = c.recv(1024)
try:
  f =  open(filename, 'rb')
  content = f.read()
  print(content)
  
  # Gửi dữ liệu trong file cho client
  c.send(content)
  f.close()
  
except FileExistsError:
  c.send("File not found") #nếu file không tồn tại bảo với client rằng "File not found"


  
c.close()
