import socket
import pygame
import threading

from client_config import *
from comms.Comms import Comms
from server.Host import Host
from objects.ObjectManager import ObjectManager
from game.game_config import *
from graphics.gfx_config import *
from objects.gui_overlays import *
from objects.Sprites import *


class Game:
    """A game class that interacts with the ObjectManager and layers the sprites."""
    def __init__(self, field_width: int, field_height: int, offset: tuple):
        """
        Initializes a Game Object.
        
        :param field_width: The width of the field to draw sprites on.
        :param field_height: The height of the field to draw sprites on.
        :param offset: The offset distance to place the field from the window border
                       (offset from top right corner).
        """
        self.gui_items_list = []
        self.objects_list = {}
        self.buttons_list = []
        self.message = []
        self.gui_overlay_state = gui_overlay.MAIN_MENU
        self.player_id = None
        self.comms = Comms()
        self.object_manager = ObjectManager(self.comms)
        self.main_menu = main_menu()
        self.lobby = lobby()
        self.pause_screen = pause_screen()
        self.character_selection_screen = character_pick()
        self.tick = 0
        self.IS_RUNNING = True
        self.sprites_list = pygame.sprite.Group()

    # def parse(self, message: str):
    #     """
    #     De-serializes the message and runs functions associated with the packet contents.

    #     :param message: The message to de-serialize.
    #     """
    #     if not message: return
    #     packets = message.split(" ")
    #     for packet in packets:
    #         contents = packet.split("+")
    #         packet_type = contents[0]
    #         if packet_type == "$ID":
    #             self.client_id = int(contents[1])
    #         if packet_type == "$START":
    #             self.gui_overlay_state = gui_overlay.NONE
    #             self.player_id = int(contents[1])
    #             print(self.player_id)
    #             pass
    #         if packet_type == "$MAP":
    #             self.object_manager.load_map(contents[1])
    #         if packet_type == "$UPP":
    #             self.objects_list[int(contents[1])].x_pos = int(contents[2])
    #             self.objects_list[int(contents[1])].y_pos = int(contents[3])
    #             self.objects_list[int(contents[1])].direction = bool(int(contents[4]))
    #             self.objects_list[int(contents[1])].status = int(contents[5])
    #             self.objects_list[int(contents[1])].status_effect = int(contents[6])
    #         if packet_type == "$OBJ":
    #             pass
    
    def get_data_to_send(self): return self.message

    def next_sprite_id(self): return len(self.objects_list.items()) - 1

    def run(self):
        """Runs all ongoing Game functions in a single tick."""
        # self.client.reset_message()
        packet_list = self.comms.parse()
        self.object_manager.parse(packet_list)
        self.parse(packet_list)


        self.sprites_list.empty()
        self.gui_items_list.clear()
        self.buttons_list.clear()
        # self.message = []

        # * Networking
        # if self.IS_HOST:
        #     self.receive_data(self.server.receive(self.competitor_client_id,
        #                                                        self.server.clients[self.competitor_client_id][0]))
        #     self.server.add_packet_to_message(["$T" + str(self.tick)])
        # if not self.IS_HOST:
        #     self.receive_data(self.client.receive(self.tick))
        #     self.client.add_packet_to_message(["$R" + str(self.tick)])
        

        # * Run ObjectManager
        self.object_manager.run(self.tick)

        # * Load GUI Elements
        if self.gui_overlay_state == gui_overlay.MAIN_MENU:
            elements, buttons = self.main_menu.load_elements()
            for element in elements + buttons:
                self.gui_items_list.append(element)
            for button in buttons:
                self.buttons_list.append(button)
        if self.gui_overlay_state == gui_overlay.LOBBY:
            elements, buttons = self.lobby.load_elements()
            for element in elements + buttons:
                self.gui_items_list.append(element)
            for button in buttons:
                self.buttons_list.append(button)
        if self.gui_overlay_state == gui_overlay.PAUSE_SCREEN:
            elements, buttons = self.pause_screen.load_elements()
            for element in elements + buttons:
                self.gui_items_list.append(element)
            for button in buttons:
                self.buttons_list.append(button)
        if self.gui_overlay_state == gui_overlay.CHARACTER_SELECTION:
            elements, buttons = self.character_selection_screen.load_elements()
            for element in elements + buttons:
                self.gui_items_list.append(element)
            for button in buttons:
                self.buttons_list.append(button)
        self.check_buttons((-1, -1), False)


        self.tick += 1
    
        for _, object in self.object_manager.background_list.items():
            self.sprites_list.add(object)
        for _, object in self.object_manager.bottom_particles.items():
            self.sprites_list.add(object)
        for _, object in self.object_manager.players.items():
            self.sprites_list.add(object)
        for _, object in self.object_manager.other_objects.items():
            self.sprites_list.add(object)
        for _, object in self.object_manager.top_particles.items():
            self.sprites_list.add(object)
        for _, object in self.object_manager.in_game_ui.items():
            self.sprites_list.add(object)
        for element in self.gui_items_list:
            self.sprites_list.add(element)
        self.sprites_list.update()

        

    def load_map(self, map_id: int):
        """
        Loads the map into the background.
        
        :param map_id: The ID of the map to load.
        """
        self.objects_list.clear()
        self.objects_list[self.next_sprite_id()] = Map(self.next_sprite_id, map_id)

    def check_buttons(self, cursor_position: tuple, MOUSE_CLICKED: bool):
        """
        Checks the state of and animates buttons.

        :param cursor_position: A tuple containing the location of the mouse cursor.
        :param MOUSE_CLICKED: A boolean for whether the mouse button was pressed.
        """
        if self.gui_overlay_state == gui_overlay.MAIN_MENU:
            for button in self.main_menu.buttons_list:
                button.check_button(cursor_position, MOUSE_CLICKED)
                if button.function == button_type.HOST_GAME and button.IS_PRESSED:

                    # TODO: Make host ALSO a Client of the Server (like before but this time it 
                    # TODO: only syncs player status)
                    self.IS_HOST = True
                    self.lobby.set_host_state(self.IS_HOST)
                    self.host = Host()
                    self.hosted_game_thread = threading.Thread(target=self.host.run)
                    self.hosted_game_thread.start()
                    self.comms_thread = threading.Thread(target=self.comms.run)
                    self.comms.connect('localhost')
                    self.comms_thread.start()
                    self.gui_overlay_state = gui_overlay.LOBBY
                if button.function == button_type.DIRECT_CONNECT and button.IS_PRESSED:
                    self.comms_thread = threading.Thread(target=self.comms.run)
                    self.comms.connect('192.168.1.15')
                    self.comms_thread.start()
                    self.gui_overlay_state = gui_overlay.LOBBY
        if self.gui_overlay_state == gui_overlay.LOBBY:
            for button in self.lobby.buttons_list:
                button.check_button(cursor_position, MOUSE_CLICKED)
                if button.function == button_type.START_GAME and button.IS_PRESSED:
                    map_id = self.object_manager.get_map_id()
                    self.start()
        if self.gui_overlay_state == gui_overlay.PAUSE_SCREEN:
            pass
        if self.gui_overlay_state == gui_overlay.CHARACTER_SELECTION:
            for button in self.character_selection_screen.buttons_list:
                button.check_button(cursor_position, MOUSE_CLICKED)
                if button.function == button_type.STICKMAN_CHARACTER and button.IS_PRESSED:
                    self.comms.send_character("stickman")

    def parse(self, packets: list):
        """Runs functions associated with the packet contents."""
        if not packets: return
        for packet in packets:
            contents = packet.split("+")
            packet_type = contents[0]
            if packet_type == "$CHARPICK":
                self.gui_overlay_state = gui_overlay.CHARACTER_SELECTION
            if packet_type == "$ID":
                self.player_id = int(contents[1])
            if packet_type == "$STARTGAME":
                self.gui_overlay_state = gui_overlay.NONE

    def quit(self):
        self.comms.quit()

    def start(self):
        """Sends start message to server."""
        # self.client.add_packet_to_message(["$START"])
        self.comms.start_game()
        pass