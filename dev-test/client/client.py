import socket

class Client:
    def __init__(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 6010
        self.client_id = None


        # States
        self.IS_CONNECTED = False
    
    def connect(self, address):

        self.socket.connect((address, self.port))
        self.socket.send(bytes("", "utf-8"))
        self.IS_CONNECTED = True

    def receive(self):
        # if not self.IS_CONNECTED: return
        try:
            msg = self.socket.recv(1024).decode("utf-8")
            print(msg)
            print("yes")
            self.parse(msg)
        except socket.error as message:
            print("CLIENT could not receive:", message)

    def send(self, **kwargs):
        
        # if not self.IS_CONNECTED: return
        message = kwargs.get('message', "")
        message = "+".join([" ".join(["$ID", str(self.client_id)]), message, "$DUMMY"])
        print(message)
        if not self.IS_CONNECTED:
            message = "+".join([message, "$QUIT"])
            print(message)

        try:
            self.socket.send(bytes(message, "utf-8"))
        except socket.error as message:
            print("CLIENT could not send:", message)

    
    def parse(self, message: str):
        # print(message)
        packets = message.split("+")
        for packet in packets:
            contents = packet.split(" ")
            for index, item in enumerate(contents):
                if item == "$ID":
                    self.client_id = contents[1]
                if item == "$DUMMY":
                    pass
                if item == "$UPDATE":
                    disconnected_client = contents[index+1]
                    if self.client_id > disconnected_client:
                        self.client_id += 1
    
    def disconnect(self):
        self.IS_CONNECTED = False
        self.send()
        self.socket.close()