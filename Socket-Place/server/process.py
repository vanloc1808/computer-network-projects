import socket
import json

from cv2 import add

def send_file(sock, address, file_name):
    f = open(file_name, 'rb')

    content = f.read()

    sock.send(content)

    f.close()

def query_all_places(sock, address):
    result = []
    # load json file
    database_file = open('db.json', 'r')
    data = json.load(database_file)

    # read data from json file
    for place in data:
        id = place['id']
        name = place['name']

        this_place = {'ID:' : id, 'Name' : name}
        # print(this_place)

        result.append(this_place)

    # close the file
    database_file.close()

    # print(result)

    sock.sendto(json.dumps(result, ensure_ascii=False).encode('utf-8'), address)

def query_one_place(sock, address, place_id):
    # load json file
    database_file = open('db.json', 'r')
    data = json.load(database_file)

    this_place = None

    # read data from json file
    for place in data:
        if place['id'] == place_id:
            id = place['id']
            name = place['name']
            description = place['description']
            this_place = {'ID:' : id, 'Name' : name, 'Description' : description}
            break

    # close the file
    database_file.close()

    sock.sendto(json.dumps(this_place, ensure_ascii=False).encode('utf-8'), address)


def main():
    localIP     = "127.0.0.1"
    localPort   = 20001
    bufferSize  = 1024

    # Create a datagram socket
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    # Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))

    print("UDP server up and listening")

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]
    place_id = message.decode('utf-8')
    print(type(place_id))
    print(place_id)

    address = bytesAddressPair[1]

    query_one_place(UDPServerSocket, address, place_id)
    
    UDPServerSocket.close()

main()

def test_send_file():
    BLOCK_SIZE = 1024

    host = 'localhost'
    port = 6767


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print("Server listening on port", port)

    c, addr = s.accept()

    place_id = c.recv(1024)

    # query_all_places(c)

    query_one_place(c, place_id.decode('utf-8'))
    
    c.close()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen(1)
    print("Server listening on port", port)

    c, addr = s.accept()

    place_id = c.recv(1024)
    send_file(c, './images/' + place_id.decode('utf-8') + '/avt.jpg')

    c.close()