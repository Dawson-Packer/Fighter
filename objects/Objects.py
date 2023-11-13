import pygame as pygame
import math as math
import objects.Sprites as Sp
from config import *

def facing(direction: int, player, object):
    if object.x_pos > player.x_pos and direction > 0 or\
    object.x_pos < player.x_pos and direction < 0: return True
    else: return False

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

        @param char_name    The name of the Player's character.
        @param player    The player id (1 or 2).
        @param x_pos    The x-position on the screen of the player.
        @param y_pos    The y-position on the screen of the player (top-down).
        @param rotation    The rotational value of the player.
        @param objectid    The ID of the Player object.
        @param height    The height of the sprite to draw.
        @param width    The width of the sprite to draw.
        """
        super().__init__(height, width, x_pos, y_pos, rotation, object_id, "s", "0.png", char_name)
        self.direction_right = True
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.ground = y_pos
        self.health = 100.0
        self.hitbox_height = height - 30
        self.basic_attack_offset_height = [26, 0]
        self.x_velocity = 0.0
        self.y_velocity = 0.0
        self.move_cooldown = 0
        self.punch_cooldown = 0
        self.kick_cooldown = 0

        self.tick()
        if player == 2:
            self.direction_right = False
            self.flip_texture(True, False)


    def move(self, direction: int):
        """
            Set the player's horizontal velocity to the direction specified
            (0 - left, 1 - right, 2 - jump).
        """
        match direction:
            case 0:
                self.x_velocity = -15.0
            case 1:
                self.x_velocity = 15.0
            case 2:
                if self.y_pos == self.ground:
                    self.anim_tick_j = 0
                    self.y_velocity = 35.0

    # Moves
    def duck(self):
        if self.status != player_status.PLAYER_JUMPING:
            self.status = player_status.PLAYER_DUCKING

    def punch(self, direction: int, player, amount):

        if self.punch_cooldown == 0:
            if self.direction_right and direction == -1:
                self.direction_right = not self.direction_right
                self.flip_texture(True, False)
                self.move_cooldown = 3
            elif not self.direction_right and direction == 1:
                self.direction_right = not self.direction_right
                self.flip_texture(True, False)
                self.move_cooldown = 3
            self.status = player_status.PLAYER_PUNCHING
            self.anim_tick_p = 0
            if abs(player.x_pos - self.x_pos) < 70 and\
            (self.y_pos - self.basic_attack_offset_height[0]) >=\
                (player.y_pos - player.hitbox_height) and facing(direction, self, player):
                player.damage(amount)
            self.punch_cooldown = 5
            print(self.y_pos - self.basic_attack_offset_height[0], player.y_pos - player.hitbox_height)
            print(abs(player.x_pos - self.x_pos) < 70)
            print(facing(direction, self, player))

    
    def kick(self, direction: int, player, amount):

        if self.kick_cooldown == 0:
            if self.direction_right and direction == -1:
                self.direction_right = not self.direction_right
                self.flip_texture(True, False)
                self.move_cooldown = 3
            elif not self.direction_right and direction == 1:
                self.direction_right = not self.direction_right
                self.flip_texture(True, False)
                self.move_cooldown = 3
            self.status = player_status.PLAYER_KICKING
            self.anim_tick_k = 0
            if abs(player.x_pos - self.x_pos) < 70 and\
            (self.y_pos - self.basic_attack_offset_height[1]) >=\
                (player.y_pos - player.hitbox_height) and facing(direction, self, player):
                player.damage(amount)
            self.kick_cooldown = 20
        print(self.y_pos - self.basic_attack_offset_height[1], player.y_pos - player.hitbox_height)

    def process_physics(self):
        """Change the Player's position due to its velocity."""

        if self.move_cooldown == 0:
            if self.y_velocity != 0.0:
                self.status = player_status.PLAYER_JUMPING
            self.y_pos -= self.y_velocity
            if self.y_pos > self.ground:
                self.y_pos = self.ground
                self.y_velocity = 0.0
            if self.y_pos < self.ground:
                self.y_velocity -= 9.8

            if self.y_velocity == 0.0:
                if (self.x_velocity < 0 and self.direction_right) or\
                (self.x_velocity > 0 and not self.direction_right):
                    self.direction_right = not self.direction_right
                    self.flip_texture(True, False)
                if self.x_velocity != 0.0: self.status = player_status.PLAYER_WALKING
                self.x_pos += self.x_velocity
                self.x_velocity = 0.0

                if self.x_pos - (self.width / 2) < 0.0: self.x_pos = 0.0 + (self.width / 2)
                elif self.x_pos + (self.width / 2) > 1000.0: self.x_pos = 1000.0 - (self.width / 2)

        
        self.update_sprite(self.x_pos, self.y_pos)

    def damage(self, value: float):
        self.health -= value
        print(self.health)
        if self.health <= 0.0: self.die()

    def die(self):
        print("Player died")

    def tick(self):
        """Execute actions every tick for the player."""
        self.status = player_status.PLAYER_STANDING
        if self.move_cooldown > 0: self.move_cooldown -= 1
        if self.punch_cooldown > 0: self.punch_cooldown -= 1
        if self.kick_cooldown > 0: self.kick_cooldown -= 1


class Crit(Sp.Sprite):
    def __init__(self,
                 crit_type: str,
                 x_pos: float,
                 y_pos: float,
                 rotation: float,
                 object_id: int,
                 height: int,
                 width: int
                 ):
        """
        @brief    Crit object child of Sprite. Summoned during an attack

        @param crit_type    The type of Crit to display.
        @param x_pos    The x-position on the screen of the Crit.
        @param y_pos    The y-position on the screen of the Crit (top-down).
        @param rotation    The rotational value of the Crit.
        @param object_id    The ID of the Crit object.
        @param height    The height of the Crit to draw.
        @param width    The width of the Crit to draw.
        """
        super().__init__(height, width, x_pos, y_pos, rotation, object_id, "default", crit_type + ".png", "crit")