import socket
import json

BLOCK_SIZE = 1024

host = 'localhost'
port = 6767

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((host, port))
s.listen(1)
print("Server listening on port", port)

c, addr = s.accept()

filename = c.recv(1024)

def query_all_places(sock):
    result = []
    # load json file
    database_file = open('db.json', 'r')
    data = json.load(database_file)

    # read data from json file
    for place in data:
        id = place['id']
        name = place['name']
        description = place['description']

        this_place = {'ID:' : id, 'Name' : name, 'Description' : description}
        # print(this_place)

        result.append(this_place)

    # close the file
    database_file.close()

    # print(result)

    sock.send(json.dumps(result, ensure_ascii=False).encode('utf-8'))

query_all_places(c)

