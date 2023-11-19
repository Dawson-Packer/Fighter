import socket
import time

from game_config import *


class Server:
    def __init__(self, max_connections: int):
        """
        Start local server and bind to port.

        :param max_connections: The maximum number of connections allowed on the server.
        """
        self.IS_RUNNING = True
        self.HOSTED_GAME = None
        self.GAME_RUNNING = False
        self.MAX_CONNECTIONS = max_connections
        self.keypresses = []
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
        self.message = [["+$DUMMY"]]
        
        self.clients = []
        self.users = []
        self.CLIENT_CONNECTIONS_SATURATED = False

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
        for client, address in self.clients:
            self.send(client, message=f"+$UPDATE {client_id}")
        print(len(self.clients))
        self.clients.pop(client_id) if self.clients else False
    
    # def start(self, game_id: int):
    #     """
    #     Start the server.

    #     :param game_id: The game to be hosted on the server.
    #     """
    #     self.HOSTED_GAME = game_id
    #     self.run()

    def run(self):
        """Run the server operations for the game."""
        # self.listening_thread = threading.Thread(target=self.listen, args=(game_type,))
        # self.listening_thread.start()
        self.received_message = ""
        if self.num_connections() == 0: self.clients.clear()
        if not self.CLIENT_CONNECTIONS_SATURATED:
            try:
                self.listen()
            except socket.timeout: pass
        if self.MAX_CONNECTIONS == self.num_connections() and\
            not self.GAME_RUNNING:
            self.CLIENT_CONNECTIONS_SATURATED = True
            self.GAME_RUNNING = True
            self.add_packet_to_message(["$STARTGAME", "0"])
        else: self.CLIENT_CONNECTIONS_SATURATED = False

        # if not self.num_connections() == 0:
        #     # print(self.num_connections())
        #     self.received_message = ""
        #     for client, address in self.clients:
        #         # print(client)
        #         self.receive(client)



            # for client, address in self.clients:
            #     # print(client)
            #     self.send(client)

    def listen(self):
        """Listen for connections to the server."""
        # print("LISTENING")
        try:
            self.socket.listen(1)
            clientsocket, address = self.socket.accept()
            self.clients.append((clientsocket, address))
            # self.users.append(str(len(self.clients) - 1))
            print(f'Client {address} successfully connected!')
            self.send(clientsocket, message=f"$ID {self.next_client_id()}")
        except socket.timeout: pass

    def receive(self, client: socket):
        """
        Receive message from a client specified.

        :param client: The client socket to read data from.
        :returns: The decoded message from the client.
        """
        try:
            message = client.recv(1024).decode("utf-8")
            # self.received_message = self.received_message + "_" + message
            # print(self.received_message)
        except socket.error as message:
            print("SERVER could not receive:", message)
        return message

    def add_packet_to_message(self, packet: list):
        self.message.append(packet)

    def send(self, client_socket: socket, *args, **kwargs):
        # force_message = kwargs.get('message', "")
        # self.message.append(force_message)
        try:
            if 'message' in kwargs:
                client_socket.send(bytes("+".join([kwargs.get('message', "")]), "utf-8"))
            else:
        # try:
                client_socket.send(bytes("+".join([" ".join(x) for x in self.message]), "utf-8"))
        except socket.error as message:
            print("SERVER could not send:", message)
        # TODO: Empty message list default (SEE TOP)
        self.message = [["+$DUMMY"]]

    def stop(self):
        """Stop the server."""
        self.IS_RUNNING = False

    # def send_object_data(self, objects: list):
        
