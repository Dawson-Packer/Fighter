import socket

from client.Game import Game

class Client(Game):
    def __init__(self):

        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 6010
        self.client_id = None
        self.message = [[]]


        # States
        self.IS_CONNECTED = False
    
    def connect(self, address):

        self.socket.connect((address, self.port))
        self.socket.send(bytes("", "utf-8"))
        self.IS_CONNECTED = True

    def receive(self):
        if not self.IS_CONNECTED: return
        try:
            msg = self.socket.recv(1024).decode("utf-8")
            # print(msg)
            self.parse(msg)
        except socket.error as message:
            print("CLIENT could not receive:", message)

    def send(self, *args, **kwargs):
        try:
            if 'message' in kwargs:
                self.socket.send(bytes("+".join([f"+ID {self.client_id}",
                                                 kwargs.get('message', "")]), "utf-8"))
            else:
                if len(self.message) > 0: self.message.insert(0, [f"$ID {self.client_id}"])
                else: self.message = [[f"$ID {self.client_id}"]]
                if not self.IS_CONNECTED:
                    self.message.append(["$QUIT"])
                # print(self.message)
                
                self.socket.send(bytes("+".join([" ".join(x) for x in self.message]), "utf-8"))
        except socket.error as message:
            print("CLIENT could not send:", message)
        self.message = [[]]

    
    def parse(self, message: str):
        # print(message)
        packets = message.split("+")
        for packet in packets:
            contents = packet.split(" ")
            packet_type = contents[0]
            if packet_type == "$ID":
                self.client_id = contents[1]
            if packet_type == "$DUMMY":
                pass
            if packet_type == "$STARTGAME":
                print(f"{self.client_id} received STARTGAME command")
            if packet_type == "$UPDATE":
                disconnected_client = contents[1]
                if self.client_id > disconnected_client:
                    self.client_id += 1
            if packet_type == "$OBJ":
                pass
    
    def disconnect(self):
        self.IS_CONNECTED = False
        self.send()
        self.socket.close()