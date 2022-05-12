import socket
import timer

localIP     = "127.0.0.1"
localPort   = 20001
bufferSize  = 10

# msgFromServer       = "Hello UDP Client"
# bytesToSend         = str.encode(msgFromServer)

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# UDPServerSocket.timeout = 5

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))
print(f"[+] UDP server ready! {(localIP, localPort)}")

# Listen for incoming datagrams
while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address, port = bytesAddressPair[1]
    clientMsg = "Message from Client:{}".format(message)
    clientIP  = f"Client IP Address:{(address, port)}"
    print(clientMsg)
    print(clientIP)

    if message == b'handshake\n':
        UDPServerSocket.sendto(b'ACK', (address, port))
        UDPServerSocket.settimeout(5.0)
        try:
            receive = UDPServerSocket.recvfrom(bufferSize)
        except socket.timeout as e:
            print("Timed out!")
        UDPServerSocket.settimeout(None)

    # Sending a reply to client
    # 
