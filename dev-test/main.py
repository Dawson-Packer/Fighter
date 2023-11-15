from server.server import Server
from client.client import Client
import time
import threading
import os
from game_config import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():  
    server = Server()
    client = Client()
    
    th1 = threading.Thread(target=server.run, args=[game_id.GAME_TEST])
    th1.start()

    client.connect('localhost')

    for _ in range(0, 5):
        client.receive()
        client.send()

        time.sleep(0.5)

    th1.join()
    # game = Application("Fighter", 1000, 600)

    # th1 = th.Thread(target=<function name>)
    # th1.start()
    # while game.isRunning:
    #     game.tick()
    #     time.sleep(game.delay)
        
    # th1.join()
    

if __name__ == '__main__':
    main()