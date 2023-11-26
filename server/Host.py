import time

from .Server import Server

class Host:
    """Hosts a local server and manages connections."""
    def __init__(self) -> None:
        self.server = Server()
        self.tick = 0

    def run(self):
        while self.server.IS_RUNNING:
            start_time = time.time()
            self.server.reset_message()
            self.server.run()
            for client_id, (client, _) in enumerate(self.server.clients):
                message = self.server.receive(client_id, client)
                self.parse(client_id, message)
            

            for client_id, (client, _) in enumerate(self.server.clients):
                self.server.send(client, client_id=client_id)
            
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
            if packet_type[:2] != "$R":
                self.server.add_packet_to_message(contents)