import os as os
import pygame as pygame
from config import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, height: int,
                 width: int,
                 x_pos: float,
                 y_pos: float,\
                rotation: float,
                sprite_id: int,
                category: int,
                file_name: str,
                name: str
                ):
        """
        @brief    Initializes a base class Sprite used to store basic data for elements loaded to
                  the screen or running in the background.

        @param height    The height of the Sprite to draw.
        @param width    The width of the Sprite to draw.
        @param x_pos    The x-position on the screen of the Sprite.
        @param y_pos    The y-position on the screen of the Sprite (top-down).
        @param rotation    The rotational value of the Sprite.
        @param sprite_id    The ID of the Sprite.
        @param category    The category of the texture of the Sprite.
        @param file_name    The file name of the Sprite image.
        @param name    The display name of the Sprite.
        """
        super().__init__()


        self.set_texture(name, category, file_name, width, height)

        self.display_x = None
        self.display_y = None
        self.rotation = None
        self.width = width
        self.height = height
        self.set_rotation(rotation)
        self.ID = sprite_id
        self.name = name

        self.update_sprite(x_pos, y_pos)

    def set_rotation(self, r: float):
        """Set the rotation of the sprite on the screen to the rounded value of the actual position."""
        self.rotation = r
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()


    def get_rotation(self): 
        """Return the rotation value of the Sprite."""
        return self.rotation


    def update_sprite(self, x: float, y: float):
        """
        @brief    Updates the sprite information using the data in the Sprite instance.

        @param x    The actual x-position of the object.
        @param y    The actual y-position of the object.
        """
        self.display_x = round(x)
        self.display_y = round(y)
        self.rect.x = self.display_x - (self.width // 2)
        self.rect.y = self.display_y - (self.height // 2)


    def set_texture(self, char_name: str, category: str, file_name: str, width: int, height: int):
        """
        @brief    Sets the texture of the Sprite to the texture specified by the parameters.

        @param char_name    The name of the character to pull the texture from.
        @param category    The category of the image.
        @param file_name    The name of the file to load.
        @param width    The width of the image to load.
        @param height    The height of the image to load.
        """
        self.image = pygame.transform.smoothscale(pygame.image.load(os.path.join("assets", "texture", char_name, category, file_name)).convert_alpha(), (width, height))
        self.rect = self.image.get_rect()


    def flip_texture(self, x_axis: bool, y_axis):
        """Flip the texture of the Sprite on the axis specified."""
        if x_axis:
            self.image = pygame.transform.flip(self.image, True, False)
        if y_axis:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()


class AnimatedSprite(Sprite):
    def __init__(self, height: int,
                 width: int,
                 x_pos: float,
                 y_pos: float,\
                rotation: float,
                sprite_id: int,
                category: int,
                file_name: str,
                name: str
                ):
        """
        @brief    Initializes an AnimatedSprite which contains animation functionality on top of
                  the base Sprite class.

        @param height    The height of the Sprite to draw.
        @param width    The width of the Sprite to draw.
        @param x_pos    The x-position on the screen of the Sprite.
        @param y_pos    The y-position on the screen of the Sprite (top-down).
        @param rotation    The rotational value of the Sprite.
        @param sprite_id    The ID of the Sprite.
        @param category    The category of the texture of the Sprite.
        @param file_name    The file name of the Sprite image.
        @param name    The display name of the Sprite.
        """
        super().__init__(height, width, x_pos, y_pos, rotation, sprite_id, category, file_name, name)
        self.anim_tick_s = 0
        self.anim_tick_w = 0
        self.anim_tick_j = 0
        self.anim_tick_p = -1
        self.anim_tick_k = -1
        self.anim_tick_d = 0

    
    def animate(self, xFlipped: bool, yFlipped: bool):
        """
        @brief    Changes the texture of the AnimatedSprite per tick with the texture specific to
                  its state.

        @param xFlipped    A boolean indicating whether the texture is flipped horizontally.
        @param yFlipped    A boolean indicating whether the texture is flipped vertically.
        """
        if self.anim_tick_p != -1: self.status = player_status.PLAYER_PUNCHING
        if self.anim_tick_k != -1: self.status = player_status.PLAYER_KICKING

        match self.status:
            case player_status.PLAYER_STANDING:
                self.set_texture(self.name, "s", str(self.anim_tick_s // 4) + ".png",
                                 self.width, self.height)
            case player_status.PLAYER_WALKING:
                self.set_texture(self.name, "w", str(self.anim_tick_w // 2) + ".png",
                                 self.width, self.height)
            case player_status.PLAYER_JUMPING:
                self.set_texture(self.name, "j", str(self.anim_tick_j) + ".png",
                                 self.width, self.height)
            case player_status.PLAYER_PUNCHING:
                self.set_texture(self.name, "p", str(self.anim_tick_p) + ".png",
                                 self.width, self.height)
            case player_status.PLAYER_KICKING:
                self.set_texture(self.name, "k", str(self.anim_tick_k) + ".png",
                                 self.width, self.height)
            case player_status.PLAYER_DUCKING:
                self.set_texture(self.name, "d", str(self.anim_tick_d) + ".png",
                                 self.width, self.height)
                
        if xFlipped:
            self.flip_texture(True, False)
        if yFlipped:
            self.flip_texture(False, True)
        self.update_sprite(self.x_pos, self.y_pos)
        # Tick counter
        self.anim_tick_s += 1
        if self.anim_tick_s == 7: self.anim_tick_s = 0
        self.anim_tick_w += 1
        if self.anim_tick_w == 7: self.anim_tick_w = 0
        self.anim_tick_j += 1
        if self.anim_tick_j == 4: self.anim_tick_j = 0
        if self.anim_tick_p >= 0: self.anim_tick_p += 1
        if self.anim_tick_p == 3: self.anim_tick_p = -1
        if self.anim_tick_k >= 0: self.anim_tick_k += 1
        if self.anim_tick_k == 3: self.anim_tick_k = -1
        self.anim_tick_d += 1
        if self.anim_tick_d == 1: self.anim_tick_d = 0

