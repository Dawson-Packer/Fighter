import time
import random

from .game_config import *
from graphics.gfx_config import *
from .objects.Objects import *
# from game_config import *



class ObjectManager:
    """A manager class that runs the game logic and interacts with the game objects."""
    def __init__(self):
        """
        Initializes an ObjectManager object.
        
        :param field_width: The width of the field to contain the game objects.
        :param field_height: The height of the field to contain the game objects.
        """
        self.server = Server()

        self.next_object_id = 0
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

    def run(self, tick: int):
        """Runs all ongoing object management functions in a single tick."""
         
        ## * Process objects.
        for _, player in self.players.items():
            player.tick()


        
        ## * Load objects

    def get_map_id(self):
        return random.randint(0, 0)

    def load_map(self, map_id: int):
        self.background_list[self.next_object_id] = 0

    def load_players(self):

        # Player 0 object
        self.players[self.next_object_id] = StickmanCharacter(self.next_object_id,
                                                              self.server,
                                                              200.0,
                                                              200.0,
                                                              True,
                                                              0.0,
                                                              0.
                                                              )
        self.next_object_id += 1
        # Player 1 object
        self.players[self.next_object_id] = StickmanCharacter(self.next_object_id,
                                                              self.server,
                                                              800.0,
                                                              200.0,
                                                              False,
                                                              0.0, 
                                                              0.0
                                                              )
        self.next_object_id += 1