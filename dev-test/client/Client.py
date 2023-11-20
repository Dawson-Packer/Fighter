import socket


class Client:
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
        if self.lost_connection(): return
        try:
            message = self.socket.recv(1024).decode("utf-8")
            # print(msg)
            # TODO: Move parse out of receive, make receive return message
            # self.parse(message)
            return message
        except socket.error as message:
            print("CLIENT could not receive:", message)
            self.packets_lost += 1
            return ""

    def send(self, *args, **kwargs):
        if not self.IS_CONNECTED: return
        try:
            if 'message' in kwargs:
                self.socket.send(bytes("+".join([" ".join(x) for x in 
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
    
    def lost_connection(self) -> bool:
        """Return True if the client has lost connection to the server."""
        MAX_PACKET_LOSS_ALLOWABLE = 10
        if self.packets_lost > MAX_PACKET_LOSS_ALLOWABLE:
            self.IS_CONNECTED = False
            return True
        else: return False
    
    # def add_packet_to_message(self, packet: list):
    #     """
    #     Add a packet of information to the global message sent to the server by the client.

    #     :param packet: A list of items, starting with the tag ($___) to send as a packet.
    #     """
    #     self.message.append(packet)

    def disconnect(self):
        self.IS_CONNECTED = False
        self.send()
        self.socket.close()
