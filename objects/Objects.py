from comms.Comms import Comms
from .Sprites import *

class Object:
    def __init__(self, object_id: int, x_pos: float, y_pos: float, type: int):
        self.object_id = object_id
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.type = type


class PhysicsObject(Object):
    def __init__(self, object_id: int, x_pos: float, y_pos: float,
                 x_velocity: float, y_velocity: float, type: int):
        super().__init__(object_id, x_pos, y_pos, type)
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity
        self.move_cooldown = 0
        self.ground = 175

    def process_physics(self, status: int, hitbox_height: int, hitbox_width: int):
        """
        Changes the Player's position due to its velocity.
        
        :param status: The status of the PhysicsObject.
        :param hitbox_height: The height of the PhysicsObject's hitbox.
        :param hitbox_width: The width of the PhysicsObject's hitbox.
        """
        can_change_status = True
        if status == player_status.PUNCHING or status == player_status.KICKING:
            can_change_status = False
        if self.move_cooldown == 0:
            if self.y_velocity != 0.0:
                if can_change_status: status = player_status.IN_AIR
            self.y_pos += self.y_velocity
            if self.y_pos < self.ground:
                self.y_pos = self.ground
                self.y_velocity = 0.0
            if self.y_pos > self.ground:
                self.y_velocity -= 9.8

            if self.y_velocity == 0.0 and self.x_velocity != 0.0:
                if status != player_status.MOVING_SLOW:
                    if can_change_status: status = player_status.MOVING
                self.x_pos += self.x_velocity
            elif self.y_velocity == 0.0 and self.x_velocity == 0.0 and not status == player_status.DUCKING:
                if can_change_status: status = player_status.IDLE
            self.x_velocity = 0.0

            # TODO: Replace hardcoded boundaries
        if self.x_pos - (hitbox_width / 2) < 0.0: self.x_pos = 0.0 + (hitbox_width / 2)
        elif self.x_pos + (hitbox_width / 2) > 1000.0: self.x_pos = 1000.0 - (hitbox_width / 2)
        return status


class Projectile(PhysicsObject):
    """Projectile Object that stores data for the projectile."""
    def __init__(self, object_id: int, radius: float, x_pos: float, y_pos: float,
                 x_velocity: float, y_velocity: float):
        """
        Initializes a Projectile object.

        :param object_id: The ID of the Object.
        :param radius: The radius of the projectile.
        :param x_pos: The x-position of the player.
        :param y_pos: The y-position of the player.
        :param direction: The initial direction of the player.
        :param x_velocity: The initial x-velocity of the player.
        :param y_velocity: The initial y-velocity of the player.
        """
        super().__init__(object_id, x_pos, y_pos, x_velocity, y_velocity, 1)
        self.radius = radius