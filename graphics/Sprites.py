import os as os
import pygame as pygame

from .gfx_config import *
from game.game_config import *
from client_config import *

class Sprite(pygame.sprite.Sprite):
    """Base class Sprite for storing positional texture data."""
    def __init__(self, height: int,
                 width: int,
                 x_pos: int,
                 y_pos: int,\
                 rotation: float,
                 sprite_id: int,
                 type: int,
                 **kwargs
                ):
        """
        Initializes a base class Sprite used to store basic data for elements loaded to
        the screen or running in the background.

        :param height: The height of the Sprite to draw.
        :param width: The width of the Sprite to draw.
        :param x_pos: The x-position on the screen of the Sprite.
        :param y_pos: The y-position on the screen of the Sprite (top-down).
        :param rotation: The rotational value of the Sprite.
        :param sprite_id: The ID of the Sprite.
        :param type: The type of sprite (player, map, gui).
        """
        super().__init__()

        if 'character' in kwargs:
            self.character = kwargs.get('character', "")
        if 'state' in kwargs:
            self.texture_state = kwargs.get('state', "")
        if 'map' in kwargs:
            self.map = kwargs.get('map', "")
        if 'element' in kwargs:
            self.gui_element = kwargs.get('element', "")
        self.type = type
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.set_texture()
        self.rotation = None
        self.set_rotation(rotation)
        self.id = sprite_id

        self.update_sprite()

    def set_rotation(self, r: float):
        """
        Sets the rotation of the sprite on the screen to the rounded value of the actual position.
        """
        self.rotation = r
        self.image = pygame.transform.rotate(self.image, self.rotation)
        self.rect = self.image.get_rect()


    def get_rotation(self): 
        """Returns the rotation value of the Sprite."""
        return self.rotation


    def update_sprite(self):
        """Updates the sprite information using the data in the Sprite instance."""
        self.rect.x = self.x_pos - (self.width // 2)
        self.rect.y = self.y_pos - (self.height // 2)


    def set_texture(self):
        """
        Sets the texture of the Sprite to the texture specified by the parameters.

        :param type: The type of sprite to add a texture to.
        :param width: The width of the image to load.
        :param height: The height of the image to load.
        """
        if self.type == sprite_type.PLAYER:
            self.image = pygame.transform.smoothscale(
                pygame.image.load(os.path.join("assets",
                                               "textures",
                                               self.character,
                                               self.texture_state,
                                               "0.png")).convert_alpha(),
                                               (self.width, self.height))
        elif self.type == sprite_type.MAP:
            self.image = pygame.transform.smoothscale(
                pygame.image.load(os.path.join("assets",
                                               "textures",
                                               "map",str(self.map) +
                                               ".png")).convert_alpha(),
                                               (self.width, self.height))
        elif self.type == sprite_type.GUI:
            self.image = pygame.transform.smoothscale(
                pygame.image.load(os.path.join("assets",
                                               "textures",
                                               "gui",
                                               str(self.gui_element) +
                                               ".png")).convert_alpha(),
                                               (self.width, self.height))
        self.rect = self.image.get_rect()
        self.update_sprite()


    def flip_texture(self, x_axis: bool, y_axis):
        """Flips the texture of the Sprite on the axis specified."""
        if x_axis:
            self.image = pygame.transform.flip(self.image, True, False)
        if y_axis:
            self.image = pygame.transform.flip(self.image, False, True)
        self.rect = self.image.get_rect()


class AnimatedSprite(Sprite):
    """Child class AnimatedSprite of Sprite that handles animations."""
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
        Initializes an AnimatedSprite object which contains animation functionality on top of
        the base Sprite class.

        :param height: The height of the Sprite to draw.
        :param width: The width of the Sprite to draw.
        :param x_pos: The x-position on the screen of the Sprite.
        :param y_pos: The y-position on the screen of the Sprite (top-down).
        :param rotation: The rotational value of the Sprite.
        :param sprite_id: The ID of the Sprite.
        :param category: The category of the texture of the Sprite.
        :param file_name: The file name of the Sprite image.
        :param name: The display name of the Sprite.
        """
        super().__init__(height, width, x_pos, y_pos, rotation, sprite_id, category, file_name, name)
        self.anim_tick_s = 0
        self.anim_tick_w = 0
        self.anim_tick_j = 0
        self.anim_tick_p = -1
        self.anim_tick_k = -1
        self.anim_tick_d = 0
        self.anim_tick_c = 0

    
    def animate(self, xFlipped: bool, yFlipped: bool):
        """
        Changes the texture of the AnimatedSprite per tick with the texture specific to
        its state.

        :param xFlipped: A boolean indicating whether the texture is flipped horizontally.
        :param yFlipped: A boolean indicating whether the texture is flipped vertically.
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
            case player_status.PLAYER_CROUCHING:
                self.set_texture(self.name, "c", str(self.anim_tick_c // 4) + ".png",
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
        if self.anim_tick_p == 3:
            self.status = player_status.PLAYER_STANDING
            self.anim_tick_p = -1
        if self.anim_tick_k >= 0: self.anim_tick_k += 1
        if self.anim_tick_k == 3:
            self.status = player_status.PLAYER_STANDING
            self.anim_tick_k = -1
        self.anim_tick_d += 1
        if self.anim_tick_d == 1: self.anim_tick_d = 0
        self.anim_tick_c += 1
        if self.anim_tick_c == 15: self.anim_tick_c = 0

class Player(AnimatedSprite):
    """Player object child of Sprite. Represents the player on screen."""
    def __init__(self,
                 character_name: str,
                 player: int,
                 x_pos: float,
                 y_pos: float,
                 rotation: float,
                 object_id: int,
                 height: int,
                 width: int
                 ):
        """
        Initializes a player object

        :param character_name: The name of the Player's character.
        :param player: The player id (1 or 2).
        :param x_pos: The x-position on the screen of the player.
        :param y_pos: The y-position on the screen of the player (top-down).
        :param rotation: The rotational value of the player.
        :param object_id: The ID of the Player object.
        :param height: The height of the sprite to draw.
        :param width: The width of the sprite to draw.
        """
        super().__init__(height, width, x_pos, y_pos, rotation, object_id,
                         "s", "0.png", character_name)
        self.direction = True
        self.STATUS_CHANGED = False
        self.status = -1

class Map(Sprite):
    """Map class for storing the ID of the map loaded."""
    def __init__(self,
                 map_id
                ):
        """
        Initializes a Map object that holds the data for the background.

        :param map_id: The ID of the map to display.
        """
        super().__init__(window_properties.HEIGHT, window_properties.WIDTH,
                         window_properties.WIDTH / 2, window_properties.HEIGHT / 2, 0.0, -1,
                         sprite_type.MAP, map=map_id)

        self.map_id = map_id

class Button(Sprite):
    """Button class used to operate the GUI."""
    def __init__(self, height: int,
                 width: int,
                 x_pos: int,
                 y_pos: int,
                contents: str,
                function: int
                ):
        """
        Initializes a Button object.

        :param height: The height of the Button to draw.
        :param width: The width of the Button to draw.
        :param x_pos: The x-position on the screen of the Button.
        :param y_pos: The y-position on the screen of the Button (top-down).
        :param contents: The display name of the Button.
        :param function: The type of button function.
        """
        super().__init__(height, width, x_pos, y_pos, 0.0, -1, sprite_type.GUI, element='button')

        self.contents = contents
        self.press_state = 0
        self.function = function
        self.IS_PRESSED = False

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
                self.set_texture()
                self.update_sprite()
        elif self.press_state == 1: self.press_state += 1
        elif self.press_state == 2: self.press_state += 1
        elif self.press_state == 3:
            self.gui_element += '_pressed'
            self.set_texture()
            self.press_state += 1
        elif self.press_state == 4: self.press_state += 1
        elif self.press_state == 5:
            self.press_state += 1
            self.depress()
        elif self.press_state == 6:
            self.IS_PRESSED = True
            self.press_state = 0
            
    
    def depress(self):
        self.gui_element = self.gui_element[:-8]
        self.set_texture()