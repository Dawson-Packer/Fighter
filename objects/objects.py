import pygame as pygame
import math as math
import objects.Sprites as Sp
from config import *


class Player(Sp.AnimatedSprite):
    def __init__(self, 
                 char_name: str,
                 player: int,
                 x_pos: float,
                 y_pos: float,
                 rotation: float,
                 object_id: int,
                 height: int,
                 width: int
                 ):
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
        super().__init__(height, width, x_pos, y_pos, rotation, object_id, "s", "0.png", char_name)
        self.direction_right = True
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.ground = y_pos
        self.x_velocity = 0.0
        self.y_velocity = 0.0
        self.reset_player_status()
        if player == 2:
            self.direction_right = False
            self.flip_texture(True, False)
        if self.direction_right == False: print(player)

    def move(self, direction: int):
        """
            Set the player's horizontal velocity to the direction specified
            (0 - left, 1 - right, 2 - jump).
        """
        match direction:
            case 0:
                self.x_velocity = -10.0
            case 1:
                self.x_velocity = 10.0
            case 2:
                if self.y_pos == self.ground: self.y_velocity = 30.0

    def process_physics(self):
        """Change the Player's position due to its velocity."""

        if (self.x_velocity < 0 and self.direction_right) or\
           (self.x_velocity > 0 and not self.direction_right):
            self.direction_right = not self.direction_right
            self.flip_texture(True, False)
        if self.x_velocity != 0.0: self.status = player_status.PLAYER_WALKING
        self.x_pos += self.x_velocity
        self.x_velocity = 0.0

        if self.x_pos - (self.width / 2) < 0.0: self.x_pos = 0.0 + (self.width / 2)
        elif self.x_pos + (self.width / 2) > 1000.0: self.x_pos = 1000.0 - (self.width / 2)

        self.y_pos -= self.y_velocity
        if self.y_pos > self.ground:
            self.y_pos = self.ground
            self.y_velocity = 0.0
        if self.y_pos < self.ground:
            self.y_velocity -= 9.8
        self.update_sprite(self.x_pos, self.y_pos)

    
    def reset_player_status(self):
        """Reset the player status to standing."""
        self.status = player_status.PLAYER_STANDING