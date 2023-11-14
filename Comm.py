import socket

class Communication:
    def __init__(self):
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.host = 'localhost'
            self.port = 6001
            self.socket.bind((self.host, self.port))

            self.socket.listen(5)
        except socket.error as message:
            print("Socket failed to bind:", message)
    

    def listen_for_connections(self):
        self.socket.listen(5)
        self.connection, self.connection_address = self.socket.accept()

    def direct_connect(self, ip_address: str):
        host = ip_address
        port = 6001
        try:

            self.remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.remote_socket.connect((host, port))


        
        except socket.error as message:
            print("Direct connect failed:", message)

    def receive(self):
        connection, address = self.socket.accept()

        data = connection.recv(1024)

        print(data.decode("uft-8"))