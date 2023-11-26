from .GameObjects import *
from comms.Comms import Comms


class StickmanCharacter(Player):
    """Stickman Character Object that stores data for unique character functions."""
    def __init__(self, object_id: int, comms: Comms, x_pos: float, y_pos: float, direction: bool,
                 x_velocity: float, y_velocity: float, sprite_height: int, sprite_width: int,
                 rotation: float):
        """
        Initializes a StickmanCharacter object.

        :param object_id: The ID of the Object.
        :param comms: The communication service to use.
        :param x_pos: The x-position of the Player.
        :param y_pos: The y-position of the Player.
        :param direction: The initial direction of the Player.
        :param x_velocity: The initial x-velocity of the Player.
        :param y_velocity: The initial y-velocity of the Player.
        :param sprite_height: The height of the Sprite.
        :param sprite_width: The width of the Sprite.
        :param rotation: The rotation of the Sprite.
        """
        hitbox_height = 50
        hitbox_width = 20
        super().__init__(object_id, comms, x_pos, y_pos, direction, x_velocity, y_velocity, hitbox_height,
                         hitbox_width, sprite_height, sprite_width, "stickman", rotation)

    def move_1(self):
        pass

    def move_2(self):
        pass

    def move_3(self):
        pass

    def ultimate(self):
        pass