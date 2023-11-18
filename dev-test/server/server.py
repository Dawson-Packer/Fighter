import socket
import threading
import time
from game_config import *

class Server:
    def __init__(self):
        """Start local server and bind to port."""
        self.IS_RUNNING = True
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host = ''
            self.port = 6010
            self.socket.bind((self.host, self.port))
            self.socket.settimeout(0.005)
        except socket.error as message:
            print("Socket bind error:", message)
        
        self.clients = []
        self.users = []
        self.CLIENT_CONNECTIONS_SATURATED = False

    def num_connections(self):
        """Return the number of clients connected to the server."""
        return len(self.clients)
    
    def next_client_id(self):
        """Return the ID of the next client connected."""
        return len(self.clients) - 1
    
    def run(self, game_type: int):
        """
        Start server operations for the game.
        :param game_type    The game to be hosted on the server.
        """
        # self.listening_thread = threading.Thread(target=self.listen, args=(game_type,))
        # self.listening_thread.start()
        while self.IS_RUNNING:
            if not self.CLIENT_CONNECTIONS_SATURATED:
                try:
                    self.listen()
                except socket.timeout: pass
                if game_type == game_id.GAME_TEST and self.num_connections() == 1:
                    self.CLIENT_CONNECTIONS_SATURATED = True
                elif game_type == game_id.GAME_1V1 and self.num_connections() == 2:
                    self.CLIENT_CONNECTIONS_SATURATED = True
                elif game_type == game_id.GAME_COMPETITION and self.num_connections() == 16:
                    self.CLIENT_CONNECTIONS_SATURATED = True
                else: self.CLIENT_CONNECTIONS_SATURATED = False
            print("yes")
            if not self.num_connections() == 0:
                print(self.num_connections())
                for client, address in self.clients:
                    print(client)
                    self.receive()

                for client, address in self.clients:
                    print(client)
                    self.send(client)

                time.sleep(0.010)            

    def listen(self):
        """Listen for connections to the server."""
        print("LISTENING")
        try:
            self.socket.listen(1)
            clientsocket, address = self.socket.accept()
            self.clients.append((clientsocket, address))
            self.users.append(str(len(self.clients) - 1))
            print(f'Client {address} successfully connected!')
            clientsocket.send(bytes(f"+$ID {self.next_client_id()}", "utf-8"))
        except socket.timeout: pass

    def receive(self):
        try:
            msg = self.clients[0][0].recv(1024).decode("utf-8")
            print(msg)
            self.parse(msg)
        except socket.error as message:
            print("SERVER could not receive:", message)

    def send(self, client_socket: socket, *args, **kwargs):
        message = kwargs.get('message', "")

        try:
            client_socket.send(bytes("+$DUMMY", "utf-8"))
        except socket.error as message:
            print("SERVER could not send:", message)

    
    def parse(self, message: str):
        for client in message.split("_"):
            packets = message.split("+")
            # print(packets)
            for packet in packets:
                contents = packet.split(" ")
                for index, item in enumerate(contents):
                    if item == "$ID":
                        client_id = int(contents[1])
                        print(f"Client {client_id} sent a message")
                    if item == "$DUMMY":
                        # print("Dummy item found on server-side")
                        pass
                    if item == "$QUIT":
                        self.client_disconnected(client_id)
                    if item == "$USER":
                        # print(contents[index+1])
                        # print(client_id)
                        self.users[client_id] = contents[index+1]

    
    def client_disconnected(self, client_id: int):
        for client, address in self.clients:
            self.send(client, message=f"+$UPDATE {client_id}")
        self.clients.pop(client_id)

    
    def stop(self):
        self.IS_RUNNING = False