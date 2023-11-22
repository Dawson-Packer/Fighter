import pygame

from client.Sprites import *
from client.client_global import *

class MainMenu:
    def __init__(self):
        self.objects_list = []
        self.button_list = []
        self.message = []
        self.setup()

    def setup(self):
        background = Map("snow_blur")
        self.objects_list.append(background)

        self.host_game_button = Button(50, 100, 200, 300, "Host Game")
        self.button_list.append(self.host_game_button)
        self.objects_list.append(self.host_game_button)

        self.direct_connect_button = Button(50, 100, 600, 300, "Direct Connect")
        self.button_list.append(self.direct_connect_button)
        self.objects_list.append(self.direct_connect_button)

class Lobby:
    def __init__(self):
        self.objects_list = []
        self.button_list = []
        self.IS_HOST = False
        self.GAME_IS_STARTING = False
        # self.setup()

    def receive_data(self, message: str):
        self.parse(message)

    def parse(self, message: str):
        packets = message.split("+")
        log.enter_data([" ", message])
        # print(packets)
        for packet in packets:
            contents = packet.split(" ")
            packet_type = contents[0]
            if packet_type == "$STARTGAME":
                print("Lobby received START command")
                self.GAME_IS_STARTING = True

    def setup(self):
        background = Map("snow_blur")
        self.objects_list.append(background)

        if self.IS_HOST:
            self.start_button = Button(50, 100, 500, 300, "Start Game")
            self.button_list.append(self.start_button)
            self.objects_list.append(self.start_button)

    def tick(self):
        self.message = []
        self.add_packet_to_message(["$0"])
    
    def get_data_to_send(self): return self.message

    def add_packet_to_message(self, packet: list):
        """
        Add a packet of information to the global message sent to the server by the client.

        :param packet: A list of items, starting with the tag ($___) to send as a packet.
        """
        self.message.append(packet)