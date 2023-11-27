import socket

from Logger import Logger


class Client:
    """A Client object that sends and receives data to a server."""
    def __init__(self):
        """Initializes the Client object."""

        super().__init__()
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_port = 60010
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_port = 60020
        self.connected_ip_address = None
        self.client_id = None
        self.packets_lost = 0
        self.message = [[]]

        self.incoming_log = Logger("logs/client_incoming", ["Timestamp", "Message Received"])
        self.outgoing_log = Logger("logs/client_outgoing", ["Timestamp", "Message Sent"])


        # States
        self.IS_CONNECTED = False
    
    def connect(self, address) -> bool:
        """
        Connects the Client to a server.
        
        :param address: The IP Address of the server to connect to.
        """
        try:
            self.connected_ip_address = address
            self.tcp_socket.connect((address, self.tcp_port))
            self.tcp_socket.send(bytes("", "utf-8"))
            self.IS_CONNECTED = True
            message = self.tcp_socket.recv(1024).decode("utf-8")
            contents = message.split("+")
            self.client_id = int(contents[1])
        except socket.error as message:
            return False
        return True

    def receive(self, tick: int):
        """
        Reads data from the server.

        :param tick: The tick the Client attempted to read data during (for logging purposes only).
        """
        if self.lost_connection(): return
        try:
            message = self.tcp_socket.recv(1024).decode("utf-8")

            self.incoming_log.enter_data([tick, message])
            return message
        except socket.error as message:
            print("CLIENT could not receive:", message)
            self.packets_lost += 1
            return ""

    def receivefrom(self):
        try:
            message = self.udp_socket.recvfrom(1024)[0].decode("utf-8")
            return message
        except socket.error as message:
            print(f"Client error on reading from UDP server:", message)
            return ""

    def send(self, tick: int, *args, **kwargs):
        """
        Sends data to the server.

        :param tick: The tick the Client attempted to read data during (for logging purposes only).
        :kwargs:
         - 'message': A message to send directly to the server (overrides normal packet string).
        """
        try:
            if 'message' in kwargs:
                self.tcp_socket.send(bytes(" ".join(["+".join(x) for x in 
                                                 kwargs.get('message', "")]), "utf-8"))
                self.outgoing_log.enter_data([tick, " ".join(["+".join(x) for x in 
                                                 kwargs.get('message', "")])])

            else:
                if not self.IS_CONNECTED:
                    self.message.append(["$QUIT"])
                
                self.tcp_socket.send(bytes(" ".join(["+".join(x) for x in self.message]), "utf-8"))
                self.outgoing_log.enter_data([tick, " ".join(["+".join(x) for x in self.message])])
        except socket.error as message:
            print("CLIENT could not send:", message)
    
    def sendto(self):
        try:
            self.udp_socket.sendto(bytes(" ".join(["+".join(x) for x in self.message]), "utf-8"),
                                   (self.connected_ip_address, self.udp_port))
        except socket.error as message:
            print(f"Client could not send to UDP Server:", message)

    def lost_connection(self) -> bool:
        """Returns True if the client has lost connection to the server."""
        MAX_PACKET_LOSS_ALLOWABLE = 10
        if self.packets_lost > MAX_PACKET_LOSS_ALLOWABLE:
            self.IS_CONNECTED = False
            return True
        else: return False
    
    def add_packet_to_message(self, packet: list):
        """
        Add a packet of information to the global message sent to the server by the client.

        :param packet: A list of items, starting with the tag ($___) to send as a packet.
        """
        self.message.append(packet)

    def reset_message(self, tick: int):
        """Resets the global message of the Client."""
        self.message = [["$R" + str(tick)]]

    def disconnect(self):
        """Disconnects the Client from the server."""
        self.IS_CONNECTED = False
        self.send(-1)
        self.tcp_socket.close()
        self.udp_socket.close()
