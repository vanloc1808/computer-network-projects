import uuid
def mac_address(client):
    client.sendall(bytes(hex(uuid.getnode()), "utf8"))
    return