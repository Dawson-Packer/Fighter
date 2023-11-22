import socket

from Logger import Logger


class Server:
    def __init__(self):
        """
        Starts local server and binds to port.

        :param max_connections: The maximum number of connections allowed on the server.
        """
        print("Server started")
        self.IS_RUNNING = True
        self.GAME_RUNNING = False
        self.MAX_CONNECTIONS = 20
        self.keypresses = []
        self.tick = 0

        self.incoming_log = Logger("logs/server_incoming",
                                   ["Timestamp", "Client ID", "Message Received"])
        self.outgoing_log = Logger("logs/server_outgoing", ["Timestamp", "Message Sent"])
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host = ''
            self.port = 6010
            self.socket.bind((self.host, self.port))
            self.socket.settimeout(0.005)
        except socket.error as message:
            print("Socket bind error:", message)

        self.received_message = ""
        self.message = [["$T" + str(self.tick)]]
        
        self.clients = []
        self.ip_addresses = []
        self.packets_lost = []
        self.users = []
        self.CLIENT_CONNECTIONS_SATURATED = False

    def set_max_connections(self, max_num: int):
        """Sets the maximum number of connections to the server."""
        self.MAX_CONNECTIONS = max_num

    def num_connections(self):
        """Returns the number of clients connected to the server."""
        return len(self.clients)
    
    def next_client_id(self):
        """Returns the ID of the next client connected."""
        return len(self.clients) - 1
    
    def client_disconnected(self, client_id: int):
        """
        Re-sorts clients when a client disconnects.

        :param client_id: The ID of the client that disconnected."""
        for client, address in self.clients:
            self.send(client, message=f"+$UPDATE {client_id}")
        self.clients.pop(client_id) if self.clients else False

    def run(self):
        """Runs the server operations for the game."""
        if self.num_connections() == 0: self.clients.clear()
        if not self.CLIENT_CONNECTIONS_SATURATED:
            try:
                self.listen()
            except socket.timeout: pass
        else: self.CLIENT_CONNECTIONS_SATURATED = False
        self.tick += 1

    def listen(self):
        """Listens for connections to the server."""
        try:
            self.socket.listen(1)
            clientsocket, address = self.socket.accept()
            if not address[0] in self.ip_addresses:
                self.clients.append((clientsocket, address))
                self.ip_addresses.append(address[0])
                self.packets_lost.append(0)
            elif self.lost_connection(self.ip_addresses.index(address[0])):
                self.packets_lost[self.ip_addresses.index(address[0])] = 0
                self.clients[self.ip_addresses.index(address[0])] = (clientsocket, address)
            print(f'Client {address} successfully connected!')
            # self.send(clientsocket, message=f"$GAME {str(self.GAME_STATE)}")
        except socket.timeout: pass
        if len(self.clients) > self.MAX_CONNECTIONS: self.CLIENT_CONNECTIONS_SATURATED = True

    def receive(self, client_id: int, client: socket):
        """
        Receives a message from a client specified.

        :param client_id: The ID of the client to read data from.
        :param client: The client socket to read data from.
        :returns: The decoded message from the client.
        """
        if self.lost_connection(client_id): return ""
        try:
            client.settimeout(0.200)
            message = client.recv(1024).decode("utf-8")
            self.packets_lost[client_id] = 0
            self.incoming_log.enter_data([self.tick, client_id, message])
            return message
        except socket.error as message:
            print(f"Server error on reading from Client {client_id}:", message)
            self.packets_lost[client_id] += 1
            return ""
        
    def add_packet_to_message(self, packet: list):
        """
        Adds a packet of information to the global message sent to the clients by the server.

        :param packet: A list of items, starting with the tag ($___) to send as a packet.
        """
        self.message.append(packet)
    
    def lost_connection(self, client_id: int) -> bool:
        """Returns True if the client specified has lost connection to the server."""
        MAX_PACKET_LOSS_ALLOWABLE = 10
        if self.packets_lost[client_id] > MAX_PACKET_LOSS_ALLOWABLE: return True
        else: return False

    def send(self, client_socket: socket, *args, **kwargs):
        """
        Sends a message to a client specified.

        :param client_socket: The socket of the client to send data to.

        :kwargs:
         - 'client_id': Specify the client ID to check whether it has lost connection to the server.
         - 'message': Send a specific message rather than the global message.
        """
        if 'client_id' in kwargs:
            client_id = kwargs.get('client_id', "")
            if self.lost_connection(client_id): return
        else: client_id = None
        try:
            if 'message' in kwargs:
                client_socket.send(bytes(" ".join([kwargs.get('message', "")]), "utf-8"))
                self.outgoing_log.enter_data([self.tick, " ".join([kwargs.get('message', "")])])
            else:
                client_socket.send(bytes(" ".join(["+".join(x) for x in self.message]), "utf-8"))
                self.outgoing_log.enter_data([self.tick,
                                              " ".join(["+".join(x) for x in self.message])])
        except socket.error as message:
            print(f"Server error sending to Client {client_id}:", message)

    def reset_message(self):
        """Resets the global message of the Server."""
        self.message = [["$T" + str(self.tick)]]

    def start_game(self):
        """Sends a STARTGAME command to the clients."""
        self.CLIENT_CONNECTIONS_SATURATED = True
        self.GAME_RUNNING = True
        self.add_packet_to_message(["$STARTGAME"])

    def stop(self):
        """Stops the server."""
        print("Stopped server. . .")
        self.IS_RUNNING = False