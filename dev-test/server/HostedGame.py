import time

from server.Server import *
from server.Objects import *
from game_config import *



class HostedGame:
    def __init__(self):

        # self.GAME_TYPE = game_id
        self.server = Server()

        self.GAME_STARTING = -1


        self.user_list = []
        self.player_1 = None
        self.player_2 = None
        self.objects_list = []
        self.game_tick = -1

    def start_game(self):

        self.GAME_STARTING = False
        self.server.start_game(0)
        # Create background object
        self.create_object(object_type.BACKGROUND, 0, 500, 300, 1, "default", map_id=0)

        # Player 1 object
        self.objects_list.append(Player("stickman",
                                   0,
                                   200.0,
                                   425.0,
                                   0.0,
                                   0
                                   ))
        
        self.create_object(object_type.STICKMAN, 1, 200, 425, 1, "s")

        # Player 2 object
        self.objects_list.append(Player("stickman",
                                   1,
                                   800.0,
                                   425.0,
                                   0.0,
                                   1
                                   ))
        
        self.create_object(object_type.STICKMAN, 2, 800, 425, -1, "s")

    def create_object(self, type: int, object_id: int, x_pos: int,
                      y_pos: int, direction: int, status: int, **kwargs):
        if 'map_id' in kwargs:
            self.server.add_packet_to_message(["$CROBJ", str(type), str(object_id), str(x_pos),
                                           str(y_pos), str(direction), str(status),
                                           str(kwargs.get('map_id', ""))])
        else:
            self.server.add_packet_to_message(["$CROBJ", str(type), str(object_id), str(x_pos),
                                           str(y_pos), str(direction), str(status)])

    def tick(self):
        while self.server.IS_RUNNING:
            start_time = time.time()

            ## * Server Management.

            # Sync user list to server client list.
            # while len(self.server.clients) > len(self.user_list):
            #     self.user_list.append("USR" + str(len(self.user_list)))
                

            # Tick the server.
            self.server.run()

            ## * Start the game
            if self.GAME_STARTING == 5: self.start_game()
            if self.GAME_STARTING >= 0: self.GAME_STARTING += 1
            ## * Read and process information.
            if not self.server.num_connections() == 0:
                # Read data from each client.
                for client_id, (client, address) in enumerate(self.server.clients):
                    client_message = self.server.receive(client_id, client)
                    self.parse(client_id, client_message)
            
            ## * Start game.
            # if self.server.GAME_RUNNING and self.game_tick == -1:
            #     self.start_game()
            #     self.game_tick += 1
            
            ## * Process game physics.
            else:






                # Prepare objects for delivery.
                object_data = ["$OBJ"]
                for object in self.objects_list:
                    object_data.append(str(object.id))
                    object_data.append(str(object.character))
                    object_data.append(str(round(object.x_pos)))
                    object_data.append(str(round(object.y_pos)))
                    object_data.append(str(object.direction_right))
                    object_data.append(str(object.status.value))
                # self.server.add_packet_to_message(object_data)



                self.game_tick += 1


            ## * Send data to clients.
            for client_id, (client, address) in enumerate(self.server.clients):
                self.server.send(client, client_id=client_id)
            
            # Delay tick if execution time is less than 0.010 seconds.
            execution_time = time.time() - start_time
            if 0.010 - execution_time > 0: time.sleep(0.010 - execution_time)
        print("Outside HOSTEDGAME tick")

    def parse(self, client_id: int, message: str):
        """
        Execute actions based on the information delivered in the sent packets.

        :param client_id: The ID of the client sending the message.
        :param message: The entire message sent to the server by all the clients in one tick.
        """
        packets = message.split("+")
        # print(packets)
        for packet in packets:
            contents = packet.split(" ")
            packet_type = contents[0]
            if packet_type == "$NULL":
                print(f"Client {client_id} sent NULL request.")
                self.server.client_disconnected(client_id)
                # self.user_list.pop(client_id)
            if packet_type == "$DUMMY":
                # print("Dummy item found on server-side")
                pass
            if packet_type == "$START":
                print("Server received START command")
                self.GAME_STARTING = 0
            if packet_type == "$QUIT":
                self.server.client_disconnected(client_id)
                # self.user_list.pop(client_id)
            if packet_type == "$USER":
                self.user_list[client_id] = contents[1]
            if packet_type == "$KEY":
                pass
    
    def assign_players(self, client_1: int, client_2: int):
        self.player_1 = client_1
        self.player_2 = client_2