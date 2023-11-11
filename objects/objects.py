import pygame as pygame
import math as math
import os
import random as random

# os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Sprite(pygame.sprite.Sprite):
    def __init__(self, height: int, width: int, x: float, y: float,\
                  r: float, id: int, stage: int, file_name: str, name: str):
        """
        @brief    Base class Object used to store basic data for elements loaded to the screen or
                  running in the background.
        @param height    The height of the sprite to draw.
        @param width    The width of the sprite to draw.
        @param x    The x-position on the screen of the object.
        @param y    The y-position on the screen of the object (top-down).
        @param r    The rotational value of the object.
        @param id    The ID of the object.
        @param file_name    The file name of the sprite image.
        @param name    The display name of the object.
        """
        super().__init__()


        self.set_texture(stage, name, file_name, width, height)

        self.set_display_x(x)
        self.set_display_y(y)
        self.width = width
        self.height = height
        self.set_rotation(r)
        self.ID = id
        self.name = name

        self.rect = self.surface.get_rect()

        self.update_sprite(self.X, self.Y)

    def set_display_x(self, x: float): self.X = round(x)
    def set_display_y(self, y: float): self.Y = round(y)
    def set_rotation(self, r: float):
        self.R = r
        self.surface = pygame.transform.rotate(self.default_surface, self.R)
        self.rect = self.surface.get_rect()
        self.image = self.surface

    def display_x(self): return self.X
    def display_y(self): return self.Y
    def get_rotation(self): return self.R

    def update_sprite(self, x: float, y: float):
        """
        @brief    Updates the sprite information using the data in the Sprite instance.
        @param x    The actual x-position of the object.
        @param y    The actual y-position of the object.
        """
        self.set_display_x(x)
        self.set_display_y(y)
        self.rect.x = self.display_x() - (self.width // 2)
        self.rect.y = self.display_y() - (self.height // 2)

    def set_texture(self, stage: int, name: str, file_name: str, width: int, height: int):
        self.default_surface = pygame.transform.smoothscale(pygame.image.load(os.path.join("assets", "tex", name, stage, file_name)).convert_alpha(), (width, height))
        self.surface = self.default_surface
        self.image = self.surface


class Player(Sprite):
    def __init__(self, height: int, width: int, x: float, y: float,\
                  r: float, id: int, stage: int, file_name: str, avatar_name: str):
        """
        @brief    Player object child of Sprite. Represents the player on screen.
        @param height    The height of the sprite to draw.
        @param width    The width of the sprite to draw.
        @param x    The x-position on the screen of the player.
        @param y    The y-position on the screen of the player (top-down).
        @param r    The rotational value of the player.
        @param id    The ID of the player.
        @param file_name    The file name of the sprite image.
        @param avatar_name    The name of the avatar.
        """
        super().__init__(height, width, x, y, r, id, stage, file_name, avatar_name)
        self.x_pos = x
        self.y_pos = y
        self.ground = y
        self.x_velocity = 0.0
        self.y_velocity = 0.0

    def move(self, direction: int):
        """
        @brief    Sets the player's horizontal velocity to the direction specified
                  (0 - left, 1 - right, 2 - jump).
        """
        match direction:
            case 0:
                self.x_velocity = -10.0
            case 1:
                self.x_velocity = 10.0
            case 2:
                if self.y_pos == self.ground: self.y_velocity = 40.0

    def process_physics(self):

        self.x_pos += self.x_velocity
        self.x_velocity = 0.0
        if self.y_pos < self.ground:
            self.y_velocity -= 9.8
        self.y_pos -= self.y_velocity
        if self.y_pos > self.ground: self.y_pos = self.ground
        self.y_velocity = 0.0
        self.update_sprite(self.x_pos, self.y_pos)