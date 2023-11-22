import pygame as pygame
import random as random
import objects.Sprites as Sp
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
        self.sprites_list.empty()

        self.player_1.update_status()
        self.player_2.update_status()

        self.player_1.process_physics()
        self.player_2.process_physics()

        self.player_1.animate(not self.player_1.direction_right, False)
        self.player_2.animate(not self.player_2.direction_right, False)


        self.player_1.tick()
        self.player_2.tick()

        self.sprites_list.add(self.background)
        self.sprites_list.add(self.player_2)
        self.sprites_list.add(self.player_1)
        self.sprites_list.add(self.crit_list)

        self.sprites_list.update()
       
    def setup(self):
        """Setup specific ProgramLogic class components for this program."""
        self.sprites_list = pygame.sprite.Group()
        self.crit_list = []

        # Background Object
        self.background = Sp.Sprite(600, 1000, 500.0, 300.0, 0.0, -1, "default", "snow.png", "background")
        self.sprites_list.add(self.background)

        # Player 1 Object
        self.player_1 = obj.Player("stickman",
                                   1,
                                   200.0,
                                   425.0,
                                   0.0,
                                   1,
                                   128,
                                   128
                                   )
        # Player 2 Object
        self.player_2 = obj.Player("stickman",
                                   2,
                                   800.0,
                                   425.0,
                                   0.0,
                                   2,
                                   128,
                                   128
                                   )


    # def damage_player(self, player, amount):
    #     if amount < 10.0:
    #         self.crit_list.append(obj.Crit("yellow_star",
    #                                        player.x_pos + random.uniform(-64, 64),
    #                                        player.y_pos + random.uniform(-32, -96),
    #                                        random.uniform(0, 360.0),
    #                                        len(self.crit_list),
    #                                        24,
    #                                        24
    #                                        ))
            
        