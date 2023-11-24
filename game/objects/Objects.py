from ..game_config import *
from ..ClientComms import ClientComms
from ..Server import Server

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
        if self.move_cooldown == 0:
            if self.y_velocity != 0.0:
                status = player_status.IN_AIR
            self.y_pos += self.y_velocity
            if self.y_pos < self.ground:
                self.y_pos = self.ground
                self.y_velocity = 0.0
            if self.y_pos > self.ground:
                self.y_velocity -= 9.8

            if self.y_velocity == 0.0 and self.x_velocity != 0.0:
                if status != player_status.MOVING_SLOW:
                    status = player_status.MOVING
            self.x_pos += self.x_velocity
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


class Player(PhysicsObject):
    """Player Object that stores data for the player like health."""
    def __init__(self, object_id: int, server: Server, x_pos: float, y_pos: float, direction: bool,
                 x_velocity: float, y_velocity: float, hitbox_height: int, hitbox_width: int):
        """
        Initializes a Player object.

        :param object_id: The ID of the Object.
        :param server: The server the Player is hosted on.
        :param x_pos: The x-position of the Player.
        :param y_pos: The y-position of the Player.
        :param direction: The initial direction of the Player.
        :param x_velocity: The initial x-velocity of the Player.
        :param y_velocity: The initial y-velocity of the Player.
        :param hitbox_height: The height of the Player's hitbox.
        :param hitbox_width: The width of the Player's hitbox.
        """
        super().__init__(object_id, x_pos, y_pos, x_velocity, y_velocity, object_type.PLAYER)

        self.hitbox_height = hitbox_height
        self.hitbox_width = hitbox_width
        self.server = server
        self.comms = ClientComms(self.server, field_dimensions.HEIGHT, field_dimensions.WIDTH)
        self.status = player_status.APPEAR
        self.status_effect = 0 # TODO: Replace with config value
        self.direction = direction
        self.health = 100.0
        self.speed = 15.0

    def move(self, direction: int):
        """
        Sets the player's velocity components based on the direction specified.

        :param direction: The direction to move the player
                          (0 - left, 1 - right, 2 - jump).
        """
        match direction:
            case 0:
                self.x_velocity = -self.speed
                if self.direction: self.direction = False
            case 1:
                self.x_velocity = self.speed
                if not self.direction: self.direction = True
            case 2:
                if self.y_pos == self.ground: self.y_velocity = 35.0

    def crouch(self):
        pass

    def duck(self):
        pass

    def punch(self):
        pass
        
    def kick(self):
        pass


class StickmanCharacter(Player):
    """Stickman Character Object that stores data for unique character functions."""
    def __init__(self, object_id: int, server: Server, x_pos: float, y_pos: float, direction: bool,
                 x_velocity: float, y_velocity: float):
        """
        Initializes a StickmanCharacter object.

        :param object_id: The ID of the Object.
        :param server: The server the Player is hosted on.
        :param x_pos: The x-position of the Player.
        :param y_pos: The y-position of the Player.
        :param direction: The initial direction of the Player.
        :param x_velocity: The initial x-velocity of the Player.
        :param y_velocity: The initial y-velocity of the Player.
        """
        hitbox_height = 50
        hitbox_width = 20
        super().__init__(object_id, server, x_pos, y_pos, direction, x_velocity, y_velocity, hitbox_height,
                         hitbox_width)

    def move_1(self):
        pass

    def move_2(self):
        pass

    def move_3(self):
        pass

    def ultimate(self):
        pass