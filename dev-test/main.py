import time
import threading
import os

from server.server import Server
import server.Game as hostedgame
from client.client import Client
from game_config import *

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Main starts client (with Main Menu elements in Client [replacement to ProgramLogic])
# If start own game: start Server and connect with Client


def main():
    hosted_game = hostedgame.Game(game_id.GAME_TEST)
    client = Client()
    
    th1 = threading.Thread(target=hosted_game.tick)
    th1.start()

    client.connect('localhost')
    i = 0
    while client.IS_CONNECTED:
        i += 1
        client.receive()
        msg = ""
        if i == 300:
            client.disconnect()
            continue


        client.send()

        time.sleep(0.050)
    while True:
        pass
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