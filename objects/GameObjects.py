from ..game.game_config import *
from .Objects import *
from .Sprites import *


class Map(Sprite):
    def __init__(self, sprite_id: int, map_id):
        super().__init__(sprite_id, window_properties.HEIGHT, window_properties.WIDTH,
                         window_properties.WIDTH / 2, window_properties.HEIGHT / 2,
                         0.0, "map/" + str(map_id))
        self.map_id = map_id
    
    def tick(self):
        pass


class Button(Sprite):
    def __init__(self,
                 sprite_id: int,
                 height: int,
                 width: int,
                 x_pos: int,
                 y_pos: int,
                 contents: str,
                 function: int):
        super().__init__(sprite_id, height, width, x_pos, y_pos, 0.0, "gui/button")
        self.contents = contents
        self.press_state = 0
        self.function = function
        self.IS_PRESSED = False

    def tick(self):
        pass

    def button_pressed(self) -> bool:
        """Returns whether the Button is pressed."""
        return self.IS_PRESSED
    
    def check_button(self, cursor_position: tuple, MOUSE_CLICKED: bool):
        if self.press_state == 0:
            self.IS_PRESSED = False
            if cursor_position[0] > self.x_pos - (self.width / 2) and cursor_position[0] < self.x_pos +\
            (self.width / 2) and cursor_position[1] > self.y_pos - (self.height / 2) and\
            cursor_position[1] < self.y_pos + (self.height / 2) and MOUSE_CLICKED:
                self.press_state += 1
                self.set_texture(self.default_file_path)
                self.update_sprite()
        elif self.press_state == 1: self.press_state += 1
        elif self.press_state == 2: self.press_state += 1
        elif self.press_state == 3:
            self.default_file_path += '_pressed'
            self.set_texture(self.default_file_path)
            self.press_state += 1
        elif self.press_state == 4: self.press_state += 1
        elif self.press_state == 5:
            self.press_state += 1
            self.depress()
        elif self.press_state == 6:
            self.IS_PRESSED = True
            self.press_state = 0
            
    
    def depress(self):
        self.default_file_path = self.default_file_path[:-8]
        self.set_texture(self.default_file_path)


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

        self.update_sprite(self.x_pos, self.y_pos)

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