import time

from graphics.gfx_config import *
from game.Server import *
from game.objects.Objects import *
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
        self.user_list = []
        self.client_list = []
        self.objects_list = []
        self.game_tick = -1
        self.tick = 0

        self.FIELD_HEIGHT = field_height
        self.FIELD_WIDTH = field_width

    def start_game(self):
        """Starts the game."""

        if len(self.client_list) >= 2:
            self.assign_players(self.client_list[0], self.client_list[1])
        else: self.assign_players(self.client_list[0], -1)
        # Create background object
        self.load_map(0)
        
        # self.create_object(object_type.STICKMAN, 1, 200, 425, 1, "s")

    def load_map(self, map_id: int):
        """
        Tells the clients to load the map specified.

        :param map_id: The ID of the map to load.
        """
        self.server.add_packet_to_message(["$MAP", str(map_id)])
    
    def load_players(self):
        # Player 1 object
        # TODO: Change STANDING to DROPPING_IN, and start like 20 pixels above normal location
        self.objects_list.append(StickmanCharacter(400.0, 175, True, 0.0, 0.0))
        self.create_object(object_type.PLAYER, self.next_object_id, (200),
                           (600 - 175), direction=1, status=player_status.STANDING.value,
                           character='stickman')
        self.next_object_id += 1

    def create_object(self, type: int, object_id: int, x_pos: int,
                      y_pos: int, **kwargs):
        """
        Tells the clients to create the object specified.

        :param type: The type of object to create.
        :param object_id: The ID of the object for communication.
        :param x_pos: The initial x=position of the object.
        :param y_pos: The initial y-position of the object.
        :param direction: The initial direction of the object (True = right, False = left).
        :param status: The status of the object.
        """
        if type == object_type.PLAYER:
            self.server.add_packet_to_message(["$CROBJ",
                                               str(sprite_type.PLAYER.value),
                                               str(object_id),
                                               str(x_pos),
                                               str(y_pos),
                                               str(kwargs.get('direction', "")),
                                               str(kwargs.get('status', "")),
                                               str(kwargs.get('character', ""))
                                               ])

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
            else:


                # Process physics



                # Prepare objects for delivery.
                object_data = ["$OBJ"]
                for object in self.objects_list:
                    object_data.append(str(object.id))
                    object_data.append(str(round(self.FIELD_WIDTH - object.x_pos)))
                    object_data.append(str(round(self.FIELD_HEIGHT - object.y_pos)))
                    object_data.append(str(object.direction))
                    object_data.append(str(object.status.value))
                    object_data.append(str(object.secondary_status.value))
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