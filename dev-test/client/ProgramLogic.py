import pygame as pygame
import random as random
import time
import threading

import client.menu as menu
from client.ClientGame import ClientGame
from server.HostedGame import HostedGame
from client.Client import Client

class ProgramLogic:
    def __init__(self, field_width: int, field_height: int, offset: tuple):
        """
        @brief    The program handling, controls program objects and event functions.
        @param field_width    The width of the available space to plot.
        @param field_height    The height of the available space to plot.
        @param offset    The x and y offset from the corner of the screen to set the local
                         coordinate axii.
        """
        self.IS_RUNNING = True
        self.scene = 0
        self.last_scene = 0
        self.IS_HOSTING = False
        self.main_menu = menu.MainMenu()
        self.lobby = menu.Lobby()
        self.game = ClientGame()
        self.client = Client()
        self.sprites_list = pygame.sprite.Group()

    def tick(self):
        """Runs all functions in the program necessary in one iteration."""
        self.last_scene = self.scene

        # Main Menu
        if self.scene == 0 and self.last_scene == 0:
            self.sprites_list.empty()
            for object in self.main_menu.objects_list:
                self.sprites_list.add(object)
            if self.main_menu.host_game_button.button_pressed():
                self.main_menu.host_game_button.IS_PRESSED = False
                self.scene = 1
                if not self.IS_HOSTING:
                    self.hosted_game = HostedGame()
                    self.host_thread = threading.Thread(target=self.hosted_game.tick)
                    self.host_thread.start()
                    self.IS_HOSTING = True
                    self.lobby.IS_HOST = True
                    self.lobby.setup()
                while not self.client.IS_CONNECTED:
                    IP_Address = 'localhost'
                    success = self.client.connect(IP_Address)
                    if not success: print(f"Client failed to connect to {IP_Address}")
            if self.main_menu.direct_connect_button.button_pressed():
                self.main_menu.direct_connect_button.IS_PRESSED = False
                self.scene = 1
                while not self.client.IS_CONNECTED:
                    IP_Address = '192.168.1.15'
                    success = self.client.connect(IP_Address)
                    if not success: print(f"Client failed to connect to {IP_Address}")
        if self.scene == 1 and self.last_scene == 1:
            self.sprites_list.empty()
            for object in self.lobby.objects_list:
                self.sprites_list.add(object)
            self.lobby.receive_data(self.client.receive())
            if self.lobby.start_button.button_pressed():
                self.lobby.start_button.IS_PRESSED = False
                self.client.send(message=[["$START"]])
            if self.lobby.GAME_IS_STARTING:
                self.scene = 2
                self.game.load_map()
            

            self.lobby.tick()

            self.client.send(message=self.lobby.get_data_to_send())
        if self.scene == 2 and self.last_scene == 2:
            self.sprites_list.empty()
            self.game.receive_data(self.client.receive())

            self.game.tick()

            self.client.send(message=self.game.get_data_to_send())
            for object in self.game.objects_list:
                self.sprites_list.add(object)











        # self.player_1.animate(not self.player_1.direction_right, False)
        # self.player_2.animate(not self.player_2.direction_right, False)


        # self.player_1.tick()
        # self.player_2.tick()

        # self.sprites_list.add(self.background)
        # self.sprites_list.add(self.player_2)
        # self.sprites_list.add(self.player_1)
        # self.sprites_list.add(self.crit_list)
        self.sprites_list.update()