import time
import os

from Application import Application

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# TODO: Turn Server into a 2-socket (TCP and UDP) server where Clients hold connections to the
# TODO: TCP socket and fire fast messages to the UDP socket

def main():
    
    game = Application("Fighter", 1000, 600)
    while game.IS_RUNNING:
        game.tick()
        time.sleep(game.delay)
    

if __name__ == '__main__':
    main()