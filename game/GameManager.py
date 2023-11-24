import time

from .game_config import *
from graphics.gfx_config import *
from .ClientComms import *
from .Server import *
from .objects.Objects import *
# from game_config import *



class GameManager:
    """A manager class that runs the Server, game logic, and interacts with the game objects."""
    def __init__(self, field_width: int, field_height: int):
        """
        Initializes a GameManager object.
        
        :param field_width: The width of the field to contain the game objects.
        :param field_height: The height of the field to contain the game objects.
        """
        self.server = Server()

        self.next_object_id = 0
        self.player_1 = None
        self.player_2 = None
        self.player_list = []
        self.user_list = []
        self.client_list = []
        self.objects_list = {}
        self.game_tick = -1
        self.tick = 0

        self.FIELD_HEIGHT = field_dimensions.HEIGHT
        self.FIELD_WIDTH = field_dimensions.WIDTH
        self.comms = ClientComms(self.server, self.FIELD_HEIGHT, self.FIELD_WIDTH)

    def start_game(self):
        """Starts the game."""

        if len(self.client_list) >= 2:
            self.assign_players(self.client_list[0], self.client_list[1])
        else: self.assign_players(self.client_list[0], -1)
        self.comms.load_map(0)
    
    def load_players(self):
        # Player 1 object
        # TODO: Change STANDING to DROPPING_IN, and start like 20 pixels above normal location
        # self.player_list.append()
        # self.objects_list[self.next_object_id] = StickmanCharacter(self.next_object_id, 400.0, 175, True, 0.0, 0.0)
        self.player_list.append(StickmanCharacter(self.next_object_id, self.server, 200.0, 175.0, True, 0.0, 0.0))
        self.comms.create_object(object_type.PLAYER, self.next_object_id, 200.0,
                           175.0, direction=True, status=player_status.APPEAR,
                           character='stickman')
        self.next_object_id += 1

    def run(self):
        """Runs all ongoing game management functions in a single tick."""
        while self.server.IS_RUNNING:
            start_time = time.time()

            ## * Server Management.
            # Sync client list to server client list
            while len(self.client_list) < len(self.server.clients):
                self.client_list.append(len(self.client_list) - 1)
            # Sync user list to server client list.
            while len(self.server.clients) > len(self.user_list):
                self.user_list.append("USR" + str(len(self.user_list)))
                
            # Tick the server.
            self.server.run()

            ## * Read and process information.
            if not self.server.num_connections() == 0:
                # Read data from each client.
                for client_id, (client, address) in enumerate(self.server.clients):
                    client_message = self.server.receive(client_id, client)
                    self.parse(client_id, client_message)            
            ## * Process game physics.


                for player in self.player_list:
                    player.status = player.process_physics(player.status,
                                                           player.hitbox_height,
                                                           player.hitbox_width
                                                           )
            
                
                for player in self.player_list:
                    self.comms.update_player(player.object_id,
                                             player.x_pos,
                                             player.y_pos,
                                             player.direction,
                                             player.status,
                                             player.status_effect
                                             )
                # Increment game tick
                self.game_tick += 1

            ## * Send data to clients.
            for client_id, (client, address) in enumerate(self.server.clients):
                self.server.send(client, client_id=client_id)
            self.server.reset_message()
            
            self.tick += 1
            # Delay tick if execution time is less than 0.010 seconds.
            execution_time = time.time() - start_time
            if 0.010 - execution_time > 0: time.sleep(0.010 - execution_time)

    def parse(self, client_id: int, message: str):
        """
        Execute actions based on the information delivered in the sent packets.

        :param client_id: The ID of the client sending the message.
        :param message: The entire message sent to the server by all the clients in one tick.
        """
        if not message: return
        packets = message.split(" ")
        for packet in packets:
            contents = packet.split("+")
            packet_type = contents[0]
            if packet_type == "$NULL":
                print(f"Client {client_id} sent NULL request.")
                self.server.client_disconnected(client_id)
                # self.user_list.pop(client_id)
            if packet_type == "$DUMMY":
                pass
            if packet_type == "$START":
                print("Server received START command")
                self.start_game()
                self.server.start_game()
                self.load_players()
            if packet_type == "$QUIT":
                self.server.client_disconnected(client_id)
                # self.user_list.pop(client_id)
            if packet_type == "$USER":
                self.user_list[client_id] = contents[1]
            if packet_type == "$KEY":
                if client_id == self.player_1: self.handle_inputs(0)
                elif client_id == self.player_2: self.handle_inputs(1)
                else: print("Viewing client pressed key")
    
    def assign_players(self, client_1: int, client_2: int):
        self.player_1 = client_1
        self.player_2 = client_2
    
    def handle_inputs(self, player):
        pass