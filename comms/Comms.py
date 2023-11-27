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
        self.client_id = None
        self.IS_CONNECTED = False

    def start_game(self):
        self.client.add_packet_to_message(["$START"])

    def send_character(self, character: str):
        self.client.add_packet_to_message(["$CHAR",character])

    def send_player_data(self,
                         player_id: int,
                         x_pos: int,
                         y_pos: int,
                         direction: bool,
                         status: int,
                         status_effect: int):
        self.client.add_packet_to_message(["$UPP",
                                           str(player_id), # 1
                                           str(x_pos), # 2
                                           str(y_pos), # 3
                                           str(int(direction)), # 4
                                           str(status), # 5
                                           str(status_effect) # 6
                                           ])

    def connect(self, ip_address: str):
        while not self.client.IS_CONNECTED:
            try:
                success = self.client.connect(ip_address)
                if not success: print(f"Client failed to connect to {ip_address}")
            except socket.error as message:
                print(message)
        self.IS_CONNECTED = True
    
    def run(self):
        """
        Ticking method for Comms.

        :param tick: The tick value for the current run.
        """
        while self.client.IS_CONNECTED:
            start_time = time.time()
            self.client.reset_message(self.tick)
            self.receive(self.tick)
            self.client_id = self.client.client_id





            self.client.send(self.tick)
            self.tick += 1
            execution_time = time.time() - start_time
            if 0.010 - execution_time > 0: time.sleep(0.010 - execution_time)

    def receive(self, tick: int):
        self.message = self.client.receive(tick)
        # self.parse(self.message)

    def parse(self) -> list:
        """
        De-serializes the message and runs functions associated with the packet contents.

        :returns: A list of packets to parse.
        """
        if not self.message: return
        packets = self.message.split(" ")
        for packet in packets:
            contents = packet.split("+")
            packet_type = contents[0]
            if packet_type == "$STOP":
                self.client.disconnect()
            if packet_type == "$QUIT":
                print("Client received QUIT command from other client")
        return packets
            

    
    def quit(self):
        self.client.add_packet_to_message(["$QUIT"])