import time
import random

from .Server import Server

class Host:
    """Hosts a local server and manages connections."""
    def __init__(self) -> None:
        self.server = Server()
        self.tick = 0
        self.character_list = []
        self.username_list = []
        self.characters_selected = 0
        self.GAME_RUNNING = False

    def run(self):
        while self.server.IS_RUNNING:
            start_time = time.time()
            self.server.reset_message()
            self.server.run()
            while len(self.character_list) < len(self.server.addresses):
                self.character_list.append("null")
                self.username_list.append("USR")
            if len(self.server.addresses) > 0:
                for _ in range(len(self.server.addresses)):
                    client_id, message = self.server.receive()
                    self.parse(client_id, message)
            else:
                client_id, message = self.server.receive()
                self.parse(client_id, message)
            
            if not self.GAME_RUNNING and self.characters_selected == len(self.server.addresses) and\
                len(self.server.addresses) > 0:
                self.GAME_RUNNING = True
                self.load_game()



            self.server.send()
            
            self.tick += 1
            execution_time = time.time() - start_time
            if 0.10 - execution_time > 0: time.sleep(0.10 - execution_time)
    
    def parse(self, client_id: int, message: str):
        """
        De-serializes the message and runs functions associated with the packet contents.
        After de-serializing and processing, re-sends the message to the other clients.

        :param client_id: The ID of the client sending the message.
        :param message: The message to de-serialize.
        """
        if not message: return
        packets = message.split(" ")
        for packet in packets:
            contents = packet.split("+")
            packet_type = contents[0]
            if packet_type == "$QUIT":
                self.server.client_disconnected(client_id)
                pass
            # Sends client's message to the other clients
            # TODO: Expand this if not statement for other packets I don't want to bounce to other
            # TODO: clients.
            if packet_type == "$START":
                self.server.add_packet_to_message(["$CHARPICK"])
            if packet_type == "$CHAR":
                self.character_list[client_id] = contents[1]
                self.characters_selected += 1
            if packet_type == "$USR":
                self.username_list.append(contents[1])
            if packet_type[:2] != "$R" and packet_type != "$USR" and packet_type != "$CHAR" and\
                packet_type != "$START" and packet_type != "$ID" and packet_type != "$DUMMY":
                self.server.add_packet_to_message(contents)
    
    def load_game(self):
        p1 = 0
        p2 = 1
        map_id = random.randint(0, 0)
        map_id = 0 # TODO: REMOVE (fill in a->b range above)
        self.server.add_packet_to_message(["$PID",
                                           str(self.username_list[p1]),
                                           str(self.character_list[p1]),
                                           str(p1),
                                           str(self.username_list[p2]),
                                           str(self.character_list[p2]),
                                           str(p2)])
        
        self.server.add_packet_to_message(["$MAP", str(map_id)])
        self.server.add_packet_to_message(["$STARTGAME"])