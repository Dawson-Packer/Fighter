from client.Sprites import *
from client.Client import *
from graphics.game_config import *
from client.client_global import *
from graphics.gui_overlays import *

class ClientManager:
    def __init__(self):
        self.gui_items_list = []
        self.objects_list = []
        self.buttons_list = []
        self.message = []
        self.gui_overlay_state = gui_overlay.MAIN_MENU
        self.client = Client()
        self.main_menu = main_menu()
        self.tick = 0
        self.setup()

    def connect(self, ip_address: str):
        try:
            success = self.client.connect(ip_address)
            if not success: print(f"Client failed to connect to {ip_address}")
        except socket.error as message:
            print("Client error:", message)

    def receive_data(self, message: str):
        self.parse(message)

    def parse(self, message: str):
        # print(message)
        log.enter_data([self.tick, message])
        packets = message.split("+")
        for packet in packets:
            contents = packet.split(" ")
            packet_type = contents[0]
            if packet_type == "$ID":
                self.client_id = int(contents[1])
            if packet_type == "$DUMMY":
                pass
            if packet_type == "$STARTGAME":
                # print("Client received STARTGAME command")
                pass
            if packet_type == "$UPDATE":
                disconnected_client = int(contents[1])
                if self.client_id > disconnected_client:
                    self.client_id += 1
            if packet_type == "$MAP":
                print("Map loaded")
                self.load_map(contents[1])
            if packet_type == "$CROBJ":
                print("Object created")
                self.objects_list.append(AnimatedSprite(128, 128, int(contents[3]), int(contents[4]),
                                                        0.0, int(contents[2]), contents[6], "0.png",
                                                        contents[1]))
            if packet_type == "$OBJ":
                pass
    
    def get_data_to_send(self): return self.message

    def run(self):
        self.objects_list.clear()
        self.gui_items_list.clear()
        self.buttons_list.clear()
        self.message = []
        self.add_packet_to_message(["$R" + str(self.tick)])
        if self.gui_overlay_state == gui_overlay.MAIN_MENU:
            elements, buttons = self.main_menu.load_elements()
            for element in elements:
                self.gui_items_list.append(element)
            for button in buttons:
                self.buttons_list.append(button)

        self.check_buttons((-1, -1), False)




        self.tick += 1
    




    def add_packet_to_message(self, packet: list):
        """
        Add a packet of information to the global message sent to the server by the client.

        :param packet: A list of items, starting with the tag ($___) to send as a packet.
        """
        self.message.append(packet)

    def load_map(self, map_id: int):
        print("Loading map")
        self.objects_list.clear()

        self.objects_list.append(Map(map_id))

    def check_buttons(self, cursor_position: tuple, MOUSE_CLICKED: bool):
        if self.gui_overlay_state == gui_overlay.MAIN_MENU:
            for button in self.main_menu.buttons_list:
                print(cursor_position)
                button.check_button(cursor_position, MOUSE_CLICKED)
                if button.function == button_type.HOST_GAME and button.IS_PRESSED:
                    print("Game hosted starting!!!!!!!!!!!!!")
    
    def setup(self):
        self.objects_list.append(Map("snow_blur"))