import socket as sk
import ssl

HOSTNAME = 'pop.gmail.com'
PORT = 995

CONTEXT = ssl.create_default_context(purpose=ssl.Purpose.CLIENT_AUTH)

BLOCK_SIZE = 1024

class POP3_(object):
    def __init__(self, email: bytearray, password: bytearray) -> None:
        self.email = email
        self.password = password
        self.storedMessage = b''

        self.buffer = b'' # Handling those recv stream

        self.skSSL = None

        self.startConnection()
        self.authenticate()

    def recvStream(self): # from "real" stream to "buffer"
        temp = self.skSSL.recv(BLOCK_SIZE)
        len_data = len(temp)
        self.buffer += temp
        return len_data

    def recvallStream(self): # receive everything
        while True:
            try:
                len_data = self.recvStream()
                if len_data < BLOCK_SIZE:
                    break # Done!
            except sk.timeout:
                print("[?] Timed out")    
                break # Finished
            except sk.error:
                print("[!] Connection suddenly closed!")
                exit(1) # changed later

    def recvBuff(self, size: int): # from "buffer" to return
        if self.buffer == b'':
            self.recvallStream()
        size = min(len(self.buffer), size)
        result = self.buffer[:size] # get from top to size
        self.buffer = self.buffer[size:] # remove received block
        return result

    def unrecvBuff(self, data: bytearray): # throw data to top of buffer (unreceive)
        self.buffer = data + self.buffer

    def recvlineBuff(self):
        if self.buffer == b'':
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
        self.skSSL.send(data)

    def sendlineStream(self, data: bytearray):
        self.sendStream(data + b'\r\n')

    def authenticate(self):
        print(self.recvlineBuff()) # Gpop ready
        self.sendlineStream(b'user ' + self.email)
        print(self.recvlineBuff()) # user OK
        self.sendlineStream(b'pass ' + self.password)
        print(self.recvlineBuff()) # pass OK
        pass

    def checkMailBoxNotNull(self): # using STAT command to show how many emails left
        self.sendlineStream(b'stat')
        recv = self.recvlineBuff()
        return recv != b'+OK 0 0'

    def getTopMail(self): # Ensure you check the mailbox before doing this!!
        self.sendlineStream(b'retr 1')
        print("[!!!]")
        line = b''

        info = {}

        while line != b'.':
            line = self.recvlineBuff()
            if line[:4] == b'From':
                # 'From: an_base64_string <sender_email>'
                p = line.rfind(b'<') # find last '<' (indicating email)
                info["From"] = line[p + 1:-1] # ignore last '>' in line
            elif line[:2] == b'To':
                # 'To: receiver_email'
                info["To"] = line[4:]
            elif line[:7] == b'Subject':
                info["Subject"] = line[9:]
            # print(line)
        return info

    def startConnection(self):
        if self.skSSL != None:
            self.closeConnection()
        self.skSSL = CONTEXT.wrap_socket(sk.socket(sk.AF_INET, sk.SOCK_STREAM))
        self.skSSL.connect((HOSTNAME, PORT))
        self.skSSL.settimeout(2)
        print("[?] Connect successfully")


    def closeConnection(self):
        self.skSSL.close()
        print("[?] Disconnect successfully")