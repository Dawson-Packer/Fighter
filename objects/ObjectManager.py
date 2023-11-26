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

        self.next_object_id_counter = 0

    def run(self, tick: int):
        """Runs all ongoing object management functions in a single tick."""
         
        ## * Process objects.
        for _, player in self.players.items():
            player.tick()


        
        ## * Load objects

    def next_object_id(self):
        self.next_object_id_counter += 1
        return self.next_object_id_counter

    def get_map_id(self):
        return random.randint(0, 0)

    def load_map(self, map_id: int):
        object_id = self.next_object_id()
        self.background_list[object_id] = Map(object_id, map_id)

    def load_players(self):

        # Player 0 object
        object_id = self.next_object_id()
        self.players[object_id] = StickmanCharacter(object_id,
                                                    self.comms,
                                                    200.0,
                                                    200.0,
                                                    True,
                                                    0.0,
                                                    0.
                                                    )
        object_id = self.next_object_id()
        # Player 1 object
        self.players[object_id] = StickmanCharacter(object_id,
                                                    self.comms,
                                                    800.0,
                                                    200.0,
                                                    False,
                                                    0.0, 
                                                    0.0
                                                    )