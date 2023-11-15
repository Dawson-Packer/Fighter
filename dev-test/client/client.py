import socket

class Client:
    def __init__(self):

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 6010
        self.client_id = None
    
    def connect(self, address):

        self.socket.connect((address, self.port))
        self.socket.send(bytes("$USER DTP", "utf-8"))

    def receive(self):
        try:
            msg = self.socket.recv(1024).decode("utf-8")
            # print(msg)
        except socket.error as message:
            print("CLIENT could not receive:", message)
        self.parse(msg)

    def send(self):
        try:
            self.socket.send(bytes(f"+$ID {self.client_id}+$DUMMY", "utf-8"))
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
                    # print("Client:", self.client_id)
                if item == "$DUMMY":
                    # print("Dummy item found")
                    pass
                if item == "$UPDATE":
                    disconnected_client = contents[index+1]
                    if self.client_id > disconnected_client:
                        self.client_id += 1