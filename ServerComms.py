from Client import Client
from game.game_config import *
from graphics.gfx_config import *

class ServerComms:
    """Server Communication class that defines functions for sending data to the server."""
    def __init__(self, client: Client):
        """
        Initializes a ServerComms object.

        :param client: The client to send messages from.
        """
        self.client = client
    
    def send_keys(self, key_presses: list):
        key_W = key_presses[0]
        key_A = key_presses[1]
        key_S = key_presses[2]
        key_D = key_presses[3]
        key_SPACE = key_presses[4]
        key_LSHIFT = key_presses[5]
        key_LCTRL = key_presses[6]
        key_UP = key_presses[7]
        key_DOWN = key_presses[8]
        key_RIGHT = key_presses[9]
        key_LEFT = key_presses[10]
        self.client.add_packet_to_message(["$KEYS",
                                           str(int(key_W)), # 1 / 0
                                           str(int(key_A)), # 2 / 1
                                           str(int(key_S)), # 3 / 2
                                           str(int(key_D)), # 4 / 3
                                           str(int(key_SPACE)), # 5 / 4
                                           str(int(key_LSHIFT)), # 6 / 5
                                           str(int(key_LCTRL)), # 7 / 6
                                           str(int(key_UP)), # 8 / 7
                                           str(int(key_DOWN)), # 9 / 8
                                           str(int(key_RIGHT)), # 10 / 9
                                           str(int(key_LEFT)) # 11 / 10
                                           ])