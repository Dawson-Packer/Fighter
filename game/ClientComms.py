from .Server import Server
from .game_config import *
from graphics.gfx_config import *

class ClientComms:
    """Client Communication class that defines functions for sending data to the clients."""
    def __init__(self, server: Server, field_height, field_width):
        """
        Initializes a ClientComms object.

        :param server: The server to send messages from.
        :param field_height: The height of the playable field.
        :param field_width: The width of the playable field.
        """
        self.server = server
        self.FIELD_HEIGHT = field_height
        self.FIELD_WIDTH = field_width
    
    def load_map(self, map_id: int):
        """
        Tells the clients to load the map specified.

        :param map_id: The ID of the map to load.
        """
        self.server.add_packet_to_message(["$MAP", str(map_id)])

    def create_object(self, type: int, object_id: int, x_pos: float,
                      y_pos: float, **kwargs):
        """
        Tells the clients to create the object specified.

        :param type: The type of object to create.
        :param object_id: The ID of the object for communication.
        :param x_pos: The initial x=position of the object.
        :param y_pos: The initial y-position of the object.
        :param direction: The initial direction of the object (True = right, False = left).
        :param status: The status of the object.
        """
        if type == object_type.PLAYER:
            self.server.add_packet_to_message(["$CROBJ",
                                               str(sprite_type.PLAYER), # 1
                                               str(object_id), # 2
                                               str(round(x_pos)), # 3
                                               str(round(self.FIELD_HEIGHT - y_pos)), # 4
                                               str(kwargs.get('direction', "")), # 5
                                               str(kwargs.get('status', "")), # 6
                                               str(kwargs.get('character', "")) # 7
                                               ])
    
    def update_player(self,
                       object_id: int,
                       x_pos: float,
                       y_pos: float,
                       direction: bool,
                       status: int,
                       status_effect: int
                       ):
        if direction: direction = 1
        else: direction = 0
        self.server.add_packet_to_message(["$UPP",
                                           str(object_id), # 1
                                           str(round(x_pos)), # 2
                                           str(round(self.FIELD_HEIGHT - y_pos)), # 3
                                           str(direction), # 4
                                           str(status), # 5
                                           str(status_effect) # 6
                                           ])