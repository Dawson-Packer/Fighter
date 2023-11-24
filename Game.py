import socket
import pygame
import threading

from game.Server import Server
from game.ClientComms import ClientComms
from client_config import *
from Client import Client
from ServerComms import ServerComms
from game.ObjectManager import ObjectManager
from game.game_config import *
from graphics.gfx_config import *
from graphics.gui_overlays import *
from graphics.Sprites import *


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
        self.server = None
        self.server_comms = None
        self.client = None
        self.client_comms = None
        self.competitor_client_id = None
        self.main_menu = main_menu()
        self.object_manager = ObjectManager()
        self.lobby = lobby()
        self.tick = 0
        self.IS_RUNNING = True
        self.IS_HOST = False
        self.sprites_list = pygame.sprite.Group()

    def connect(self, ip_address: str):
        """
        Connects the Client to a server.
        
        :param ip_address: The IP Address of the server to connect to.
        """
        while not self.client.IS_CONNECTED:
            self.tick = 0
            try:
                success = self.client.connect(ip_address)
                if not success: print(f"Client failed to connect to {ip_address}")
            except socket.error as message:
                print("Client error:", message)

    def receive_data(self, message: str):
        """
        Handles the data received by the Server or Client.

        :param message: The message to parse.
        """
        self.parse(message)

    def parse(self, message: str):
        """
        De-serializes the message and runs functions associated with the packet contents.

        :param message: The message to de-serialize.
        """
        if not message: return
        packets = message.split(" ")
        for packet in packets:
            contents = packet.split("+")
            packet_type = contents[0]
            if packet_type == "$ID":
                self.client_id = int(contents[1])
            if packet_type == "$STARTGAME":
                self.gui_overlay_state = gui_overlay.NONE
                pass
            if packet_type == "$MAP":
                self.load_map(contents[1])
            if packet_type == "$UPP":
                self.objects_list[int(contents[1])].x_pos = int(contents[2])
                self.objects_list[int(contents[1])].y_pos = int(contents[3])
                self.objects_list[int(contents[1])].direction = bool(int(contents[4]))
                self.objects_list[int(contents[1])].status = int(contents[5])
                self.objects_list[int(contents[1])].status_effect = int(contents[6])
            if packet_type == "$OBJ":
                pass
    
    def get_data_to_send(self): return self.message

    def next_sprite_id(self): return len(self.objects_list.items()) - 1

    def run(self):
        """Runs all ongoing Game functions in a single tick."""
        # self.client.reset_message()
        self.sprites_list.empty()
        self.gui_items_list.clear()
        self.buttons_list.clear()
        # self.message = []

        # * Networking
        if self.IS_HOST:
            self.receive_data(self.server.receive(self.competitor_client_id,
                                                               self.server.clients[self.competitor_client_id][0]))
            self.server.add_packet_to_message(["$T" + str(self.tick)])
        if not self.IS_HOST:
            self.receive_data(self.client.receive(self.tick))
            self.client.add_packet_to_message(["$R" + str(self.tick)])

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

        if self.IS_HOST:
            # Send message to all clients in ClientComms
            pass
        if not self.IS_HOST:
            # Send message to server in ServerComms
            pass

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
                    self.IS_HOST = True
                    self.lobby.set_host_state(self.IS_HOST)
                    self.server = Server()
                    self.server_comms = ServerComms(self.client)
                    # self.host_thread = threading.Thread(target=self.hosted_game.run)
                    # self.host_thread.start()
                    # self.connect(socket.gethostname())
                    self.gui_overlay_state = gui_overlay.LOBBY
                if button.function == button_type.DIRECT_CONNECT and button.IS_PRESSED:
                    self.client = Client()
                    self.client_comms = ClientComms(self.server)
                    self.connect('192.168.1.15')
                    self.gui_overlay_state = gui_overlay.LOBBY
        if self.gui_overlay_state == gui_overlay.LOBBY:
            for button in self.lobby.buttons_list:
                button.check_button(cursor_position, MOUSE_CLICKED)
                if button.function == button_type.START_GAME and button.IS_PRESSED:
                    self.start()
        if self.gui_overlay_state == gui_overlay.PAUSE_SCREEN:
            pass

    def start(self):
        """Sends start message to server."""
        self.client.add_packet_to_message(["$START"])
    
    def send_input(self, key: str):
        self.keys_presses[key] = True