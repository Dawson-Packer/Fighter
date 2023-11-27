import socket

from Logger import Logger


class Client:
    """A Client object that sends and receives data to a server."""
    def __init__(self):
        """Initializes the Client object."""

        super().__init__()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.target_ip_address = None
        self.port = 60010
        self.connected_ip_address = None
        self.client_id = None
        self.packets_lost = 0
        self.message = [[]]

        self.incoming_log = Logger("logs/client_incoming", ["Timestamp", "Message Received"])
        self.outgoing_log = Logger("logs/client_outgoing", ["Timestamp", "Message Sent"])


        # States
        self.IS_CONNECTED = False
    
    def connect(self, ip_address) -> bool:
        """
        Connects the Client to a server.
        
        :param address: The IP Address of the server to connect to.
        """
        success = False
        self.target_ip_address = ip_address
        self.socket.sendto(bytes(" $DUMMY", 'utf-8'), (self.target_ip_address, self.port))
        message = self.socket.recvfrom(1024)[0].decode('utf-8')
        if message: success = True
        if success: self.IS_CONNECTED = True
        self.get_client_id(message)
        return success, self.client_id

    def get_client_id(self, message: str):
        if not message: return
        packets = message.split(" ")
        for packet in packets:
            contents = packet.split("+")
            packet_type = contents[0]
            if packet_type == "$ID":
                self.client_id = int(contents[1])
                print("Client's ID is", self.client_id)

    def receive(self, tick: int):
        """
        Reads data from the server.

        :param tick: The tick the Client attempted to read data during (for logging purposes only).
        """
        if self.lost_connection(): return
        try:
            message = self.socket.recvfrom(1024)[0].decode('utf-8')

            self.incoming_log.enter_data([tick, message])
            return message
        except socket.error as message:
            print("CLIENT could not receive:", message)
            self.packets_lost += 1
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
                self.socket.sendto(bytes(" ".join(["+".join(x) for x in 
                                                 kwargs.get('message', "")]), 'utf-8'),
                                                 (self.target_ip_address,
                                                 self.port))
                self.outgoing_log.enter_data([tick, " ".join(["+".join(x) for x in 
                                                 kwargs.get('message', "")])])

            else:
                if not self.IS_CONNECTED:
                    self.message.append(["$QUIT"])
                
                self.socket.sendto(bytes(" ".join(["+".join(x) for x in self.message]), 'utf-8'),
                                                 (self.target_ip_address,
                                                 self.port))
                self.outgoing_log.enter_data([tick, " ".join(["+".join(x) for x in self.message])])
        except socket.error as message:
            print("CLIENT could not send:", message)

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
        self.message = [[f"$ID+{self.client_id}"], ["$R" + str(tick)]]
        

    def disconnect(self):
        """Disconnects the Client from the server."""
        self.IS_CONNECTED = False
        self.send(-1)
        self.socket.close()
