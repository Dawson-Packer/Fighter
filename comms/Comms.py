import socket
import time

from .Client import Client


class Comms:
    def __init__(self):
        """
        Initializes a Comms object.
        """
        self.client = Client()
        self.message = None
        self.tick = 0

    def start_game(self):
        self.client.add_packet_to_message(["$START"])

    def connect(self, ip_address: str):
        while not self.client.IS_CONNECTED:
            try:
                success = self.client.connect(ip_address)
                if not success: print(f"Client failed to connect to {ip_address}")
            except socket.error as message:
                print(message)
    
    def run(self):
        """
        Ticking method for Comms.

        :param tick: The tick value for the current run.
        """
        while self.client.IS_CONNECTED:
            start_time = time.time()
            self.client.reset_message(self.tick)
            self.receive(self.tick)





            self.client.send(self.tick)
            self.tick += 1
            execution_time = time.time() - start_time
            if 0.010 - execution_time > 0: time.sleep(0.010 - execution_time)

    def receive(self, tick: int):
        message = self.client.receive(tick)
        self.parse(message)

    def parse(self, message: str):
        """
        De-serializes the message and runs functions associated with the packet contents.

        :param message: The message to de-serialize.
        """
        if not message: return
        packets = message.split(" ")
        for packet in packets:
            contents = packet.split("+")
            packet_type = contents[0]
            if packet_type == "$STOP":
                self.client.disconnect()
            if packet_type == "$QUIT":
                print("Client received QUIT command from other client")
    
    def quit(self):
        self.client.add_packet_to_message(["$QUIT"])