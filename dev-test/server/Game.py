import time

import server.server as sv
from server.Objects import *
import game_config as gc

class Game(sv.Server):
    def __init__(self, game_id: int):
        self.GAME_TYPE = game_id
        if self.GAME_TYPE == gc.game_id.GAME_TEST:
            super().__init__(1)
        elif self.GAME_TYPE == gc.game_id.GAME_1V1:
            super().__init__(2)    
        elif self.GAME_TYPE == gc.game_id.GAME_COMPETITION:
            super().__init__(16)
        self.objects_list = []
        self.game_tick = -1

    def start_game(self):

        # Player 1 object
        self.objects_list.append(Player("stickman",
                                   0,
                                   200.0,
                                   425.0,
                                   0.0,
                                   0
                                   ))
        # Player 2 object
        self.objects_list.append(Player("stickman",
                                   1,
                                   800.0,
                                   425.0,
                                   0.0,
                                   1
                                   ))

    def tick(self):
        while self.IS_RUNNING:
            start_time = time.time()
            self.run()

            if self.num_connections() == 0:
                self.clients.clear()
                self.received_message = ""
            if not self.num_connections() == 0:
            # print(self.num_connections())
                self.received_message = ""
                for client, address in self.clients:
                    # print(client)
                    self.receive(client)

            self.parse(self.received_message)
            if not self.GAME_RUNNING:
                pass
            if self.GAME_RUNNING and self.game_tick == -1:
                self.start_game()
                self.game_tick += 1
            else:

                object_data = ["$OBJ"]
                for object in self.objects_list:
                    object_data.append(str(object.id))
                    object_data.append(str(object.character))
                    object_data.append(str(round(object.x_pos)))
                    object_data.append(str(round(object.y_pos)))
                    object_data.append(str(object.direction_right))
                    object_data.append(str(object.status.value))
                # print(object_data)
                self.add_packet_to_message(object_data)

                self.game_tick += 1


            for client, address in self.clients:
                # print(client)
                self.send(client)
            
            execution_time = time.time() - start_time
            if 0.010 - execution_time > 0: time.sleep(0.010 - execution_time)

    def parse(self, message: str):
        """
        Execute actions based on the information delivered in the sent packets.

        :param message: The entire message sent to the server by all the clients in one tick.
        """
        for client in message.split("_"):
            packets = client.split("+")
            print(packets)
            for packet in packets:
                contents = packet.split(" ")
                packet_type = contents[0]
                if packet_type == "$ID":
                    client_id = int(contents[1])
                    print(f"Client {client_id} sent a message")
                if packet_type == "$DUMMY":
                    # print("Dummy item found on server-side")
                    pass
                if packet_type == "$QUIT":
                    self.client_disconnected(client_id)
                if packet_type == "$USER":
                    # print(contents[index+1])
                    # print(client_id)
                    self.users[client_id] = contents[1]
                if packet_type == "$KEY":
                    pass