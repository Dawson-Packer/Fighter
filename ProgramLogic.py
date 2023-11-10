import pygame as pygame
import objects.objects as obj

class ProgramLogic:
    def __init__(self, field_width: int, field_height: int, offset: tuple):
        """
        @brief    The program handling, controls program objects and event functions.
        @param field_width    The width of the available space to plot.
        @param field_height    The height of the available space to plot.
        @param offset    The x and y offset from the corner of the screen to set the local
                         coordinate axii.
        """
        self.isRunning = True

        self.setup()

    def tick(self, time_passed: int):
        """
        @brief    Runs all functions in the program necessary in one iteration.
        @param time_passed    The time passed since last execution.
        """

        self.player_1.process_physics()
        self.player_2.process_physics()
        self.sprites_list.update()
       
    def setup(self):
        """
        @brief    Function to setup specific ProgramLogic class components for this program, 
                  like objects.
        """
        self.sprites_list = pygame.sprite.Group()

        # Background Object
        self.background = obj.Sprite(800, 800, 400.0, 400.0, 0.0, -1, "background.png", "Background")
        self.sprites_list.add(self.background)

        # Player 1 Object
        self.player_1 = obj.Player(64, 64, 200.0, 400.0, 0.0, 1, "Robot.png", "rj")
        self.sprites_list.add(self.player_1)

        # Player 2 Object
        self.player_2 = obj.Player(64, 64, 800.0, 400.0, 0.0, 2, "Robot.png", "rj")
        self.sprites_list.add(self.player_2)