import pygame

from Game import Game
from objects.ObjectManager import ObjectManager

class UserInput:
    def __init__(self, game: Game, manager: ObjectManager) -> None:
        """
        Initializes a UserInput object.

        :param game: The Game object to point inputs at.
        :param manager: The ObjectManager object to point inputs at.
        """
        self.game = game
        self.manager = manager

    def handle_inputs(self, player_id: int):
        """
        Processes the inputs from the user and runs functions in the ObjectManager.

        :param player_id: The Player ID of the user.        
        """
        mouse_buttons_state = pygame.mouse.get_pressed(num_buttons=3)
        if mouse_buttons_state[0]:
            self.game.check_buttons(pygame.mouse.get_pos(), True)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: pass
        if keys[pygame.K_a]: self.manager.move(player_id, 0)
        if keys[pygame.K_s]: pass
        if keys[pygame.K_d]: self.manager.move(player_id, 1)
        if keys[pygame.K_SPACE]: self.manager.move(player_id, 2)
        if not keys[pygame.K_LSHIFT]:
            if keys[pygame.K_LEFT]: self.manager.punch(player_id, False)
            if keys[pygame.K_RIGHT]: self.manager.punch(player_id, True)

        if keys[pygame.K_LSHIFT]:
            if keys[pygame.K_a] or keys[pygame.K_d] and not keys[pygame.K_SPACE]:
                self.manager.crouch(player_id)
            elif keys[pygame.K_LEFT]: self.manager.kick(player_id, False)
            elif keys[pygame.K_RIGHT]: self.manager.kick(player_id, True)
            else: self.manager.duck(player_id)