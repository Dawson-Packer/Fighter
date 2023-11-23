import os as os
import pygame as pygame

from .gfx_config import *
from client_config import *

# TODO: Replace sprites with new system that's flexible for all kinds of sprites.

class Sprite(pygame.sprite.Sprite):
    """Base class Sprite for storing positional texture data."""
    def __init__(self,
                 height: int,
                 width: int,
                 x_pos: int,
                 y_pos: int,
                 rotation: float,
                 file_path: str
                 ):
        
        super().__init__()

        self.height = height
        self.width = width
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rotation = rotation
        self.rect = None

        self.set_texture(file_path)
        
    def set_texture(self, file_path: str):
        self.image = pygame.transform.smoothscale(
            pygame.image.load(os.path.join("assets",
                                           "textures",
                                           file_path,
                                           )).convert_alpha(),
                                           (self.width, self.height)
        )
        self.rect = self.image.get_rect()
        self.update_sprite()

    def update_sprite(self):
        self.rect.x = self.x_pos - (self.width // 2)
        self.rect.y = self.y_pos - (self.height // 2)

# TODO: AnimatedSprite class concatenates and sends file_path to self.set_texture by
# TODO: concatenating (character) + / + (state 0-12) + / + (tick).png
# TODO: informed by self.reset_animation(divisor: int) in AnimatedSprite