from Application import *
from Logger import *
import time
import threading as th
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def main():
    
    logger = Logger([])    

    game = Application("Fighter", 1000, 600)

    # th1 = th.Thread(target=<function name>)
    # th1.start()
    while game.isRunning:
        game.tick()
        time.sleep(game.delay)
    logger.terminate()
    # th1.join()
    

if __name__ == '__main__':
    main()
