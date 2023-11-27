import time
import random

from game.game_config import *
from graphics.gfx_config import *
from .GameObjects import *
from .Character import *
from comms.Comms import Comms
# from game_config import *



class ObjectManager:
    """A manager class that runs the game logic and interacts with the game objects."""
    def __init__(self, comms: Comms):
        """
        Initializes an ObjectManager object.
        
        :param comms: The communication service to use.
        :param field_width: The width of the field to contain the game objects.
        :param field_height: The height of the field to contain the game objects.
        """

        self.comms = comms
        self.player_id = None
        self.player_1 = None
        self.player_2 = None
        self.background_list = {}
        self.bottom_particles = {}
        self.players = {}
        self.other_objects = {}
        self.top_particles = {}
        self.in_game_ui = {}
        self.objects_list = {}
        self.game_tick = -1
        self.tick = 0
        self.player_1_info = ["USR", "null", -1]
        self.player_2_info = ["USR", "null", -1]

        self.next_object_id_counter = 0

    def run(self, tick: int):
        """Runs all ongoing object management functions in a single tick."""
        self.player_id = self.comms.client_id
        ## * Process objects.

        for _, player in self.players.items():
            if player.connected_client == self.player_id:
                self.comms.send_player_data(self.player_id,
                                            int(player.x_pos),
                                            int(player.y_pos),
                                            player.direction,
                                            player.status,
                                            player.status_effect
                                            )

        for _, player in self.players.items():
            player.tick()


        
        

    def next_object_id(self):
        self.next_object_id_counter += 1
        return self.next_object_id_counter

    def get_map_id(self):
        return random.randint(0, 0)

    def load_map(self, map_id: int):
        object_id = self.next_object_id()
        self.background_list[object_id] = Map(object_id, map_id)

    def load_players(self):

        # Player 1 object
        object_id = self.next_object_id()
        if self.player_1_info[1] == "stickman":
            self.players[object_id] = StickmanCharacter(object_id,
                                                        self.player_1_info[2],
                                                        self.comms,
                                                        200.0,
                                                        200.0,
                                                        True,
                                                        0.0,
                                                        0.0,
                                                        128,
                                                        128,
                                                        0.0
                                                        )
        object_id = self.next_object_id()
        # Player 2 object
        if self.player_2_info[1] == "stickman":
            self.players[object_id] = StickmanCharacter(object_id,
                                                        self.player_2_info[2],
                                                        self.comms,
                                                        800.0,
                                                        200.0,
                                                        False,
                                                        0.0, 
                                                        0.0,
                                                        128,
                                                        128,
                                                        0.0
                                                        )
        
    def parse(self, packets: list):
        """Runs functions associated with the packet contents."""
        if not packets: return
        for packet in packets:
            contents = packet.split("+")
            packet_type = contents[0]
            if packet_type == "$MAP":
                self.load_map(int(contents[1]))
            if packet_type == "$PID":
                self.player_1_info[0] = contents[1] # Player 1 Username
                self.player_1_info[1] = contents[2] # Player 1 Character
                self.player_1_info[2] = int(contents[3]) # Player 1 Client ID
                self.player_2_info[0] = contents[4] # Player 2 Username
                self.player_2_info[1] = contents[5] # Player 2 Character
                self.player_2_info[2] = int(contents[6]) # Player 2 Client ID
                self.load_players()
            if packet_type == "$UPP":
                for _, player in self.players.items():
                    if player.connected_client == int(contents[1]) and int(contents[1]) != self.player_id:
                        player.x_pos = int(contents[2])
                        player.y_pos = int(contents[3])
                        player.direction = bool(int(contents[4]))
                        player.status = int(contents[5])
                        player.status_effect = int(contents[6])
                        player.update_sprite(player.x_pos, player.y_pos)
    
    def move(self, player_id: int, direction: int):
        for _, player in self.players.items():
            if player.connected_client == player_id:
                player.move(direction)

    def crouch(self, player_id: int):
        for _, player in self.players.items():
            if player.connected_client == player_id:
                player.crouch()

    def duck(self, player_id):
        for _, player in self.players.items():
            if player.connected_client == player_id:
                player.duck()
    
    def punch(self, player_id: int, facing_right: bool):
        for _, player in self.players.items():
            if player.connected_client == player_id:
                player.punch(facing_right)

    def kick(self, player_id: int, facing_right: bool):
        for _, player in self.players.items():
            if player.connected_client == player_id:
                player.kick(facing_right)