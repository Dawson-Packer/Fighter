import os as os
import pygame as pygame

from .gfx_config import *
from client_config import *
from game.game_config import *

# TODO: Replace sprites with new system that's flexible for all kinds of sprites.

class Sprite(pygame.sprite.Sprite):
    """Base class Sprite for storing positional texture data."""
    def __init__(self,
                 sprite_id: int,
                 height: int,
                 width: int,
                 x_pos: int,
                 y_pos: int,
                 rotation: float,
                 file_path: str
                 ):
        """
        
        
        
        
        :param file_path: The path to the file to load from /textures/ on (excluding '.png').
        """
        
        super().__init__()

        self.id = sprite_id
        self.height = height
        self.width = width
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.default_file_path = file_path
        self.rotation = rotation
        self.rect = None

        self.set_texture(file_path)
        
    def set_texture(self, file_path: str):
        self.image = pygame.transform.smoothscale(
            pygame.image.load(os.path.join("assets",
                                           "textures",
                                           file_path + ".png"
                                           )).convert_alpha(),
                                           (self.width, self.height)
        )
        self.rect = self.image.get_rect()
        self.update_sprite()
    
    def flip_texture(self, x_axis: bool, y_axis: bool):
        if x_axis:
            self.image = pygame.transform.flip(self.image, True, False)
        if y_axis:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()
        self.update_sprite()

    def update_sprite(self):
        self.rect.x = self.x_pos - (self.width // 2)
        self.rect.y = self.y_pos - (self.height // 2)

# TODO: AnimatedSprite class concatenates and sends file_path to self.set_texture by
# TODO: concatenating (character) + / + (state 0-12) + / + (tick).png
# TODO: informed by self.reset_animation(divisor: int) in AnimatedSprite

class AnimatedSprite(Sprite):
    def __init__(self,
                 sprite_id: int,
                 height: int,
                 width: int,
                 x_pos: int,
                 y_pos: int,
                 rotation: float,
                 file_path: str
                 ):
        super().__init__(sprite_id, height, width, x_pos, y_pos, rotation, file_path)
        self.animation_tick = 0

    def animate(self, dir: str, divisor: int, cycle_end: int, facing_right: bool):
        self.set_texture(dir + str(self.animation_tick // divisor))
        if not facing_right:
            self.flip_texture(True, False)
        self.animation_tick += 1
        if self.animation_tick == cycle_end: self.animation_tick = 0
    
    def reset_tick(self):
        self.animation_tick = 0

class PlayerSprite(AnimatedSprite):
    def __init__(self,
                 sprite_id: int,
                 character: str,
                 status: int,
                 height: int,
                 width: int,
                 x_pos: int,
                 y_pos: int,
                 rotation: float,
                 direction: bool
                 ):
        super().__init__(sprite_id, height, width, x_pos, y_pos, rotation, "blank/blank")
        self.character = character
        self.status = status
        self.status_effect = None
        self.direction = direction
        self.last_direction = direction
        if not self.direction:
            self.flip_texture(True, False)

    def tick(self):
        """Ticks the Player to change attributes in time."""
        # * Animation
        if self.status ==  player_status.IDLE:
            self.animate("player/" + self.character + "/" + str(player_status.IDLE) + "/", 4, 7, self.direction)
        elif self.status == player_status.MOVING:
            self.animate("player/" + self.character + "/" + str(player_status.MOVING) + "/", 2, 7, self.direction)
        elif self.status == player_status.IN_AIR:
            self.animate("player/" + self.character + "/" + str(player_status.IN_AIR) + "/", 1, 4, self.direction)
        elif self.status == player_status.PUNCHING:
            self.animate("player/" + self.character + "/" + str(player_status.PUNCHING) + "/", 1, 3, self.direction)
        elif self.status == player_status.KICKING:
            self.animate("player/" + self.character + "/" + str(player_status.KICKING) + "/", 1, 3, self.direction)
        elif self.status == player_status.DUCKING:
            self.animate("player/" + self.character + "/" + str(player_status.DUCKING) + "/", 1, 1, self.direction)
        elif self.status == player_status.MOVING_SLOW:
            self.animate("player/" + self.character + "/" + str(player_status.MOVING_SLOW) + "/", 4, 15, self.direction)
        elif self.status == player_status.DEFENDING:
            self.animate("player/" + self.character + "/" + str(player_status.DEFENDING) + "/", 1, 1, self.direction)
        elif self.status == player_status.MOVE1:
            self.animate("player/" + self.character + "/" + str(player_status.MOVE1) + "/", 1, 1, self.direction)
        elif self.status == player_status.MOVE2:
            self.animate("player/" + self.character + "/" + str(player_status.MOVE2) + "/", 1, 1, self.direction)
        elif self.status == player_status.MOVE3:
            self.animate("player/" + self.character + "/" + str(player_status.MOVE3) + "/", 1, 1, self.direction)
        elif self.status == player_status.ULTIMATE:
            self.animate("player/" + self.character + "/" + str(player_status.ULTIMATE) + "/", 1, 1, self.direction)
        elif self.status == player_status.APPEAR:
            self.animate("player/" + self.character + "/" + str(player_status.APPEAR) + "/", 1, 1, self.direction)

        
        # Change orientation
        if self.direction != self.last_direction:
            self.flip_texture(True, False)
        self.last_direction = self.direction


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