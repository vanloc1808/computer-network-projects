import socket as sk
import ssl

HOSTNAME = 'pop.gmail.com'
PORT = 995

CONTEXT = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)

class POP3_(object):
    def __init__(self, email: bytearray, password: bytearray) -> None:
        self.email = email
        self.password = password
        self.storedMessage = b''

        self.isTimedOut = False

        self.buffer = b'' # Handling those recv stream

        self.skSSL = None

        self.startConnection()
        self.authenticate()

    def recvStream(self): # from "real" stream to "buffer"
        self.buffer += self.skSSL.recv(4096)

    def recvallStream(self): # receive everything
        while True:
            try:
                self.recvStream()
            except sk.timeout:
                self.isTimedOut = True
                break # Finished

    def recvBuff(self, size: int): # from "buffer" to return
        if not self.isTimedOut:
            self.recvallStream()
        size = min(len(self.buffer), size)
        result = self.buffer[:size] # get from top to size
        self.buffer = self.buffer[size:] # remove received block
        return result

    def unrecvBuff(self, data: bytearray): # throw data to top of buffer (unreceive)
        self.buffer = data + self.buffer

    def recvlineBuff(self):
        if not self.isTimedOut:
            self.recvallStream()

        delim = b'\r\n'

        token_pos = self.buffer.find(delim) # get position of first next line CRLF

        if token_pos == -1:
            result = self.buffer
            self.buffer = b''
            return result
        else:
            result = self.buffer[:token_pos]
            self.buffer = self.buffer[token_pos + len(delim):]
            return result

        
        pass

    def sendStream(self, data: bytearray):
        self.isTimedOut = False # send -> ready to receive new data
        self.skSSL.send(data)

    def authenticate(self):
        print(self.skSSL.recv(4096)) # Gpop ready
        self.skSSL.send(b'user ' + self.email + b'\r\n')
        print(self.skSSL.recv(4096)) # user OK
        self.skSSL.send(b'pass ' + self.password + b'\r\n')
        print(self.skSSL.recv(4096)) # pass OK
        pass

    def startConnection(self):
        if self.skSSL != None:
            self.closeConnection()
        self.skSSL = CONTEXT.wrap_socket(sk.socket(sk.AF_INET, sk.SOCK_STREAM))
        self.skSSL.connect((HOSTNAME, PORT))
        print("[?] Connect successfully")


    def closeConnection(self):
        print("[?] Disconnect successfully")
        self.skSSL.close()