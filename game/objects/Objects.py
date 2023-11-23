from game.game_config import *

class Object:
    def __init__(self, x_pos: float, y_pos: float, type: int):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.type = type


class PhysicsObject(Object):
    def __init__(self, x_pos: float, y_pos: float,
                 x_velocity: float, y_velocity: float, type: int):
        super().__init__(x_pos, y_pos, type)
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity

    def process_physics(self):
        pass


class Projectile(PhysicsObject):
    """Projectile Object that stores data for the projectile."""
    def __init__(self, radius: float, x_pos: float, y_pos: float,
                 x_velocity: float, y_velocity: float):
        """
        Initializes a Projectile object.

        :param radius: The radius of the projectile.
        :param x_pos: The x-position of the player.
        :param y_pos: The y-position of the player.
        :param direction: The initial direction of the player.
        :param x_velocity: The initial x-velocity of the player.
        :param y_velocity: The initial y-velocity of the player.
        """
        super().__init__(x_pos, y_pos, x_velocity, y_velocity, 1)
        self.radius = radius


class Player(PhysicsObject):
    """Player Object that stores data for the player like health."""
    def __init__(self, x_pos: float, y_pos: float, direction: bool,
                 x_velocity: float, y_velocity: float):
        """
        Initializes a Player object.

        :param x_pos: The x-position of the player.
        :param y_pos: The y-position of the player.
        :param direction: The initial direction of the player.
        :param x_velocity: The initial x-velocity of the player.
        :param y_velocity: The initial y-velocity of the player.
        """
        super().__init__(x_pos, y_pos, x_velocity, y_velocity, object_type.PLAYER)

        self.status = player_status.DROPPING_IN
        self.direction = direction
        self.health = 100.0
        self.speed = 15.0

        self.hitbox_height = 95

    def move(self, direction: int):
        pass

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
    def __init__(self, x_pos: float, y_pos: float, direction: bool,
                 x_velocity: float, y_velocity: float):
        """
        Initializes a StickmanCharacter object.

        :param x_pos: The x-position of the player.
        :param y_pos: The y-position of the player.
        :param direction: The initial direction of the player.
        :param x_velocity: The initial x-velocity of the player.
        :param y_velocity: The initial y-velocity of the player.
        """
        super().__init__(x_pos, y_pos, direction, x_velocity, y_velocity)

    def move_1(self):
        pass

    def move_2(self):
        pass

    def move_3(self):
        pass

    def ultimate(self):
        pass