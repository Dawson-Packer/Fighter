from client.Sprites import *
from client.Client import *
from game_config import *
from client.Logger import Logger

class ClientGame:
    def __init__(self):
        self.objects_list = []
        self.message = []
        # self.map_id = 0
        self.tick = 0
        self.setup()
        self.log = Logger(["Timestamp", "Received Message"])

    def connect(self, ip_address: str):
        try:
            success = self.client.connect(ip_address)
            if not success: print(f"Client failed to connect to {ip_address}")
        except socket.error as message:
            print("Client error:", message)

    def receive_data(self, message: str):
        self.parse(message)

    def parse(self, message: str):
        print(message)
        self.log.enter_data([self.tick, message])
        packets = message.split("+")
        for packet in packets:
            contents = packet.split(" ")
            packet_type = contents[0]
            if packet_type == "$ID":
                self.client_id = int(contents[1])
            if packet_type == "$DUMMY":
                pass
            if packet_type == "$STARTGAME":
                # print("Client received STARTGAME command")
                pass
            if packet_type == "$UPDATE":
                disconnected_client = int(contents[1])
                if self.client_id > disconnected_client:
                    self.client_id += 1
            if packet_type == "$MAP":
                print("Map loaded")
                self.load_map(contents[1])
            if packet_type == "$CROBJ":
                print("Object created")
                self.objects_list.append(AnimatedSprite(128, 128, int(contents[3]), int(contents[4]),
                                                        0.0, int(contents[2]), contents[6], "0.png",
                                                        contents[1]))
            if packet_type == "$OBJ":
                pass
    
    def get_data_to_send(self): return self.message

    def run(self):
        self.message = []
        self.add_packet_to_message(["R" + str(self.tick)])

        self.tick += 1
    
    def add_packet_to_message(self, packet: list):
        """
        Add a packet of information to the global message sent to the server by the client.

        :param packet: A list of items, starting with the tag ($___) to send as a packet.
        """
        self.message.append(packet)

    def load_map(self, map_id: int):
        print("Loading map")
        self.objects_list.clear()

        self.objects_list.append(Sprite(600, 1000, 500, 300,  0.0, -1, "default",
                                        str(map_id) + ".png", "background"))
    
    def setup(self):
        self.objects_list.append(Sprite(600, 1000, 500, 300, 0.0, -1, "default",
                                        "snow_blur.png", "background"))