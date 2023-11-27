import os as os
import pygame as pygame

from graphics.gfx_config import *
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
        Initializes a Sprite object.
          
        :param sprite_id: The ID of the Sprite object.
        :param height: The height of the Sprite texture.
        :param width: The width of the Sprite texture.
        :param x_pos: The x-position of the Sprite.
        :param y_pos: The y-position of the Sprite (top-down).
        :param file_path: The path to the file to load from /textures/ on (excluding '.png').
        """
        
        super().__init__()

        self.id = sprite_id
        self.height = height
        self.width = width
        self.display_x_pos = x_pos
        self.display_y_pos = y_pos
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

    def update_sprite(self, *args):
        """
        Updates the Sprite's rectangle position either by using either the last known position
        or a specified new position.

        :args:
         - 0: The x-position of the Object.
         - 1: The y-position of the Object.
        """
        if len(args) > 0:
            self.display_x_pos = round(args[0])
            self.display_y_pos = round(field_dimensions.HEIGHT - args[1])
        self.rect.x = self.display_x_pos - (self.width // 2)
        self.rect.y = self.display_y_pos - (self.height // 2)


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
    
    def reset_animation_tick(self):
        self.animation_tick = 0