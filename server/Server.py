import socket
import time


class Server:
    def __init__(self):
        """
        Start local server and bind to port.

        :param max_connections: The maximum number of connections allowed on the server.
        """
        self.IS_RUNNING = True
        self.GAME_RUNNING = False
        self.GAME_STATE = 0
        self.MAX_CONNECTIONS = 20
        self.keypresses = []
        self.tick = 0
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host = ''
            self.port = 6010
            self.socket.bind((self.host, self.port))
            self.socket.settimeout(0.005)
        except socket.error as message:
            print("Socket bind error:", message)

        self.received_message = ""
        # TODO: Empty message list default when timeout is set in client
        self.message = [["$T" + str(self.tick)]]
        
        self.clients = []
        self.ip_addresses = []
        self.packets_lost = []
        self.users = []
        self.CLIENT_CONNECTIONS_SATURATED = False

    def set_max_connections(self, max_num: int):
        """Set the maximum number of connections to the server."""
        self.MAX_CONNECTIONS = max_num

    def num_connections(self):
        """Return the number of clients connected to the server."""
        return len(self.clients)
    
    def next_client_id(self):
        """Return the ID of the next client connected."""
        return len(self.clients) - 1
    
    def client_disconnected(self, client_id: int):
        """
        Re-sort clients when a client disconnects.

        :param client_id: The ID of the client that disconnected."""
        print("disconnect")
        for client, address in self.clients:
            self.send(client, message=f"+$UPDATE {client_id}")
        # print(len(self.clients))
        self.clients.pop(client_id) if self.clients else False

    def run(self):
        """Run the server operations for the game."""
        if self.num_connections() == 0: self.clients.clear()
        if not self.CLIENT_CONNECTIONS_SATURATED:
            try:
                self.listen()
            except socket.timeout: pass
        # if self.MAX_CONNECTIONS == self.num_connections() and\
        #     not self.GAME_RUNNING:
        #     self.CLIENT_CONNECTIONS_SATURATED = True
        #     self.GAME_RUNNING = True
        #     self.add_packet_to_message(["$STARTGAME", "0"])
        else: self.CLIENT_CONNECTIONS_SATURATED = False
        self.tick += 1

    def listen(self):
        """Listen for connections to the server."""
        # print("LISTENING")
        try:
            self.socket.listen(1)
            clientsocket, address = self.socket.accept()
            if not address[0] in self.ip_addresses:
                self.clients.append((clientsocket, address))
                self.ip_addresses.append(address[0])
                self.packets_lost.append(0)
            else:
                self.packets_lost[self.ip_addresses.index(address[0])] = 0
                self.clients[self.ip_addresses.index(address[0])] = (clientsocket, address)
            # self.users.append(str(len(self.clients) - 1))
            print(f'Client {address} successfully connected!')
            print(address[0])
            self.send(clientsocket, message=f"$GAME {str(self.GAME_STATE)}")
        except socket.timeout: pass

    def receive(self, client_id: int, client: socket):
        """
        Receive message from a client specified.

        :param client: The client socket to read data from.
        :returns: The decoded message from the client.
        """
        if self.lost_connection(client_id): return ""
        try:
            client.settimeout(0.135)
            message = client.recv(1024).decode("utf-8")
            self.packets_lost[client_id] = 0
            return message
        except socket.error as message:
            print(f"Server error on reading from Client {client_id}:", message)
            self.packets_lost[client_id] += 1
            return ""
        
    def add_packet_to_message(self, packet: list):
        """
        Add a packet of information to the global message sent to the clients by the server.

        :param packet: A list of items, starting with the tag ($___) to send as a packet.
        """
        self.message.append(packet)
    
    def lost_connection(self, client_id: int) -> bool:
        """Return True if the client specified has lost connection to the server."""
        MAX_PACKET_LOSS_ALLOWABLE = 10
        if self.packets_lost[client_id] > MAX_PACKET_LOSS_ALLOWABLE: return True
        else: return False

    def send(self, client_socket: socket, *args, **kwargs):
        """
        Send a message to a client.

        :param client_socket: The socket of the client to send data to.

        :kwargs:
         - 'client_id': Specify the client ID to check whether it has lost connection to the server.
         - 'message': Send a specific message rather than the global message.
        """
        if 'client_id' in kwargs:
            client_id = kwargs.get('client_id', "")
            print(client_id)
            if self.lost_connection(client_id): return
        else: client_id = None
        try:
            if 'message' in kwargs:
                client_socket.send(bytes("+".join([kwargs.get('message', "")]), "utf-8"))
            else:
                print("+".join([" ".join(x) for x in self.message]))
                client_socket.send(bytes("+".join([" ".join(x) for x in self.message]), "utf-8"))
        except socket.error as message:
            print(f"Server error sending to Client {client_id}:", message)

    def reset_message(self):
        self.message = [["$T" + str(self.tick)]]

    def start_game(self, map_id: int):
        self.CLIENT_CONNECTIONS_SATURATED = True
        self.GAME_RUNNING = True
        self.add_packet_to_message(["$STARTGAME", str(map_id)])

    def stop(self):
        """Stop the server."""
        print("Stopped server")
        self.IS_RUNNING = False