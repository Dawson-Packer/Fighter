import os as os
import pygame as pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, height: int,
                 width: int,
                 x_pos: int,
                 y_pos: int,
                contents: str
                ):
        """
        Initializes a base class Button used to operate the GUI.

        :param height: The height of the Button to draw.
        :param width: The width of the Button to draw.
        :param x_pos: The x-position on the screen of the Button.
        :param y_pos: The y-position on the screen of the Button (top-down).
        :param contents: The display name of the Button.
        """
        super().__init__()

        self.x_pos = x_pos
        self.y_pos = y_pos
        self.rotation = None
        self.width = width
        self.height = height
        self.name = contents
        self.IS_PRESSED = False

        self.image = pygame.transform.smoothscale(pygame.image.load(os.path.join("assets",
                                                                                 "textures",
                                                                                 "button",
                                                                                 "button.png")).
                                                                                 convert_alpha(),
                                                                                 (self.width, self.height))
        self.rect = self.image.get_rect()
        self.update_sprite()

    def update_sprite(self):
        """Updates the sprite information using the data in the Button instance."""
        self.rect.x = self.x_pos - (self.width // 2)
        self.rect.y = self.y_pos - (self.height // 2)

    def button_pressed(self) -> bool:
        """Return whether the Button is pressed."""
        return self.IS_PRESSED
    def check_button(self, cursor_position: tuple):
        if cursor_position[0] > self.x_pos - (self.width / 2) and cursor_position[0] < self.x_pos +\
        (self.width / 2) and cursor_position[1] > self.y_pos - (self.height / 2) and\
        cursor_position[1] < self.y_pos + (self.height / 2):
            self.IS_PRESSED = True
            self.image = pygame.transform.smoothscale(pygame.image.load(os.path.join("assets",
                                                                                 "textures",
                                                                                 "button",
                                                                                 "button_pressed.png")).
                                                                                 convert_alpha(),
                                                                                 (self.width, self.height))
        self.rect = self.image.get_rect()
        self.update_sprite()
    
    def depress(self):
        self.image = pygame.transform.smoothscale(pygame.image.load(os.path.join("assets",
                                                                                 "textures",
                                                                                 "button",
                                                                                 "button.png")).
                                                                                 convert_alpha(),
                                                                                 (self.width, self.height))
        self.rect = self.image.get_rect()
        self.update_sprite()