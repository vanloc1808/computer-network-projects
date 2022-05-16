# fileclient.py

import socket 
import json

BLOCK_SIZE = 1024

def receive_all(sock):
    data = b''
    while True:
        try:
            part = sock.recv(BLOCK_SIZE)
            data += part
            if len(part) < BLOCK_SIZE:
                # either 0 or end of data
                break
        except sock.timeout:
                print("[?] Timed out")    
                break # Finished
        except sock.error:
                print("[!] Connection suddenly closed!")
                exit(1) # changed later
    
    return data

def main():
    serverAddressPort   = ("127.0.0.1", 20001)
    bufferSize          = 4096
  
    # Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Send to server using created UDP socket
    place_id = 'TRV'
    bytes_to_send = str.encode(place_id)
    UDPClientSocket.sendto(bytes_to_send, serverAddressPort)

    msgFromServer = UDPClientSocket.recvfrom(bufferSize)

    message = msgFromServer[0].decode('utf-8')
    print(message)

main()

def test_receive_file():
    place_id = 'TRV'

    s = socket.socket()
    s.connect(("localhost", 6767)) #lắng nghe ở cổng 6767


    #Gửi tên file cho server
    s.send(place_id.encode())

    image = receive_all(s)
    print(image)

    with open('testimg.jpg', 'wb') as f:
        f.write(image)
    
    s.close()
