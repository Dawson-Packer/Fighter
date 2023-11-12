import pygame as pygame
import objects.Objects as obj

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

        self.player_1.animate(not self.player_1.direction_right, False)
        self.player_2.animate(not self.player_2.direction_right, False)


        self.player_1.reset_player_status()
        self.player_2.reset_player_status()


        self.sprites_list.update()
       
    def setup(self):
        """Setup specific ProgramLogic class components for this program."""
        self.sprites_list = pygame.sprite.Group()

        # Background Object
        # self.background = obj.Sprite(800, 800, 400.0, 400.0, 0.0, -1, "d", "background.png", "bg")
        # self.sprites_list.add(self.background)

        # Player 1 Object
        self.player_1 = obj.Player("stickman",
                                   1,
                                   200.0,
                                   400.0,
                                   0.0,
                                   1,
                                   128,
                                   128
                                   )
        # Player 2 Object
        self.player_2 = obj.Player("stickman",
                                   2,
                                   800.0,
                                   400.0,
                                   0.0,
                                   2,
                                   128,
                                   128
                                   )

        self.sprites_list.add(self.player_2)
        self.sprites_list.add(self.player_1)
