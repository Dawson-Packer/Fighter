from ..game_config import *
from ..ClientComms import ClientComms
from ..Server import Server
from ...graphics.Sprites import *

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


class Player(PhysicsObject, AnimatedSprite):
    """Player Object that stores data for the player like health."""
    def __init__(self, object_id: int, server: Server, x_pos: float, y_pos: float, direction: bool,
                 x_velocity: float, y_velocity: float, hitbox_height: int, hitbox_width: int,
                 sprite_height: int, sprite_width: int, character: str, rotation: float):
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
        :param sprite_height: The height of the Sprite.
        :param sprite_width: The width of the Sprite.
        :param character: The character texture to load.
        :param rotation: The rotation of the Sprite.
        """
        PhysicsObject.__init__(self, object_id, x_pos, y_pos, x_velocity,
                               y_velocity, object_type.PLAYER)
        AnimatedSprite.__init__(self, object_id, sprite_height, sprite_width,
                                round(x_pos), round(field_dimensions.HEIGHT - y_pos),
                                rotation, "blank/blank")
        # Object Data
        self.hitbox_height = hitbox_height
        self.hitbox_width = hitbox_width
        self.server = server
        self.connected_client = None
        self.comms = ClientComms(self.server, field_dimensions.HEIGHT, field_dimensions.WIDTH)
        self.status = player_status.IDLE
        self.status_effect = 0 # TODO: Replace with config value
        self.direction = direction
        self.health = 100.0
        self.speed = 15.0

        self.move_cooldown = 0
        self.punch_cooldown = 0
        self.punch_timer = 0
        self.kick_cooldown = 0
        self.kick_timer = 0

        # Sprite Data
        self.character = character
        self.last_status = self.status
        self.last_direction = self.direction
        if not self.direction:
            self.flip_texture(True, False)


    def tick(self):
        if self.move_cooldown > 0: self.move_cooldown -= 1
        if self.punch_cooldown > 0: self.punch_cooldown -= 1
        if self.punch_timer > 0: self.punch_timer -= 1
        if self.kick_cooldown > 0: self.kick_cooldown -= 1
        if self.kick_timer > 0: self.kick_timer -= 1

        self.status = self.process_physics(self.status, self.hitbox_height, self.hitbox_width)

        self.prepare_animations()


    def prepare_animations(self):
        current_status = self.status
        if self.last_status != current_status: self.reset_animation_tick()
        if self.status ==  player_status.IDLE:
            self.animate("player/" + self.character + "/" + str(player_status.IDLE) + "/", 4, 7, self.direction)
        elif self.status == player_status.MOVING:
            self.animate("player/" + self.character + "/" + str(player_status.MOVING) + "/", 2, 7, self.direction)
            self.status = player_status.IDLE
        elif self.status == player_status.IN_AIR:
            self.animate("player/" + self.character + "/" + str(player_status.IN_AIR) + "/", 1, 4, self.direction)
            self.status = player_status.IDLE
        elif self.status == player_status.PUNCHING:
            self.animate("player/" + self.character + "/" + str(player_status.PUNCHING) + "/", 1, 3, self.direction)
            if self.animation_tick == 0: self.status = player_status.IDLE
        elif self.status == player_status.KICKING:
            self.animate("player/" + self.character + "/" + str(player_status.KICKING) + "/", 1, 3, self.direction)
            if self.animation_tick == 0: self.status = player_status.IDLE
        elif self.status == player_status.DUCKING:
            self.animate("player/" + self.character + "/" + str(player_status.DUCKING) + "/", 1, 1, self.direction)
            self.status = player_status.IDLE
        elif self.status == player_status.MOVING_SLOW:
            self.animate("player/" + self.character + "/" + str(player_status.MOVING_SLOW) + "/", 4, 15, self.direction)
            self.status = player_status.IDLE
        elif self.status == player_status.DEFENDING:
            self.animate("player/" + self.character + "/" + str(player_status.DEFENDING) + "/", 1, 1, self.direction)
        elif self.status == player_status.MOVE1:
            self.animate("player/" + self.character + "/" + str(player_status.MOVE1) + "/", 1, 1, self.direction)
            if self.animation_tick == 0: self.status = player_status.IDLE
        elif self.status == player_status.MOVE2:
            self.animate("player/" + self.character + "/" + str(player_status.MOVE2) + "/", 1, 1, self.direction)
            if self.animation_tick == 0: self.status = player_status.IDLE
        elif self.status == player_status.MOVE3:
            self.animate("player/" + self.character + "/" + str(player_status.MOVE3) + "/", 1, 1, self.direction)
            if self.animation_tick == 0: self.status = player_status.IDLE
        elif self.status == player_status.ULTIMATE:
            self.animate("player/" + self.character + "/" + str(player_status.ULTIMATE) + "/", 1, 1, self.direction)
            if self.animation_tick == 0: self.status = player_status.IDLE
        elif self.status == player_status.APPEAR:
            self.animate("player/" + self.character + "/" + str(player_status.APPEAR) + "/", 1, 1, self.direction)
            if self.animation_tick == 0: self.status = player_status.IDLE

        # Change orientation
        if self.direction != self.last_direction:
            self.flip_texture(True, False)
        self.last_status = current_status
        self.last_direction = self.direction


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
        self.speed = 15.0
        self.status = player_status.MOVING

    def crouch(self):
        self.status = player_status.MOVING_SLOW
        self.speed = 5.0

    def duck(self):
        self.status = player_status.DUCKING

    def punch(self, facing_right: bool):
        if self.punch_cooldown == 0:
            self.status = player_status.PUNCHING
            if self.direction and not facing_right:
                self.direction = False
            elif not self.direction and facing_right:
                self.direction = True
            self.move_cooldown = 3
            self.punch_cooldown = 5
            self.punch_timer = 3
        
    def kick(self, facing_right: bool):
        if self.kick_cooldown == 0:
            self.status = player_status.KICKING
            if self.direction and not facing_right:
                self.direction = False
            elif not self.direction and facing_right:
                self.direction = True
            self.move_cooldown = 3
            self.kick_cooldown = 10
            self.kick_timer = 3


class StickmanCharacter(Player):
    """Stickman Character Object that stores data for unique character functions."""
    def __init__(self, object_id: int, server: Server, x_pos: float, y_pos: float, direction: bool,
                 x_velocity: float, y_velocity: float, sprite_height: int, sprite_width: int,
                 rotation: float):
        """
        Initializes a StickmanCharacter object.

        :param object_id: The ID of the Object.
        :param server: The server the Player is hosted on.
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
        super().__init__(object_id, server, x_pos, y_pos, direction, x_velocity, y_velocity, hitbox_height,
                         hitbox_width, sprite_height, sprite_width, "stickman", rotation)

    def move_1(self):
        pass

    def move_2(self):
        pass

    def move_3(self):
        pass

    def ultimate(self):
        pass