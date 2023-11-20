import socket

from client.Game import Game

class Client(Game):
    def __init__(self):

        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 6010
        self.client_id = None
        self.packets_lost = 0
        self.message = [[]]


        # States
        self.IS_CONNECTED = False
    
    def connect(self, address) -> bool:

        try:
            self.socket.connect((address, self.port))
            self.socket.send(bytes("", "utf-8"))
            self.IS_CONNECTED = True
        except socket.error as message:
            return False
        return True

    def receive(self):
        if not self.IS_CONNECTED: return
        try:
            message = self.socket.recv(1024).decode("utf-8")
            # print(msg)
            # TODO: Move parse out of receive, make receive return message
            self.parse(message)
            return message
        except socket.error as message:
            print("CLIENT could not receive:", message)
            self.packets_lost += 1
            return ""

    def send(self, *args, **kwargs):
        if not self.IS_CONNECTED: return
        try:
            if 'message' in kwargs:
                self.socket.send(bytes("+".join([f"+ID {self.client_id}",
                                                 kwargs.get('message', "")]), "utf-8"))
            else:
                if len(self.message) > 0: self.message.insert(0, ["$0"])
                else: self.message = [["$0"]]
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
                self.client_id = int(contents[1])
            if packet_type == "$DUMMY":
                pass
            if packet_type == "$STARTGAME":
                print(f"{self.client_id} received STARTGAME command")
            if packet_type == "$UPDATE":
                disconnected_client = int(contents[1])
                if self.client_id > disconnected_client:
                    self.client_id += 1
            if packet_type == "$OBJ":
                pass
    
    def lost_connection(self) -> bool:
        """Return True if the client has lost connection to the server."""
        MAX_PACKET_LOSS_ALLOWABLE = 10
        if self.packets_lost > MAX_PACKET_LOSS_ALLOWABLE:
            self.IS_CONNECTED = False
            return True
        else: return False

    def disconnect(self):
        self.IS_CONNECTED = False
        self.send()
        self.socket.close()
