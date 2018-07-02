import sys
import time
from threading import Thread

from pren36.grab.Servomotor import Servomotor


class Launcher:
    direction = None

    def __init__(self):
        self.grabber = Servomotor()
        self.idle = True
        t_fsm = Thread(target=self.start_idle)
        t_fsm.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        try:
            if self.direction == 0:
                self.grabber.open()
            else:
                self.grabber.close()
        except KeyboardInterrupt:
            # self.grabber.stop()
            sys.exit()

    def run(self):
        if len(sys.argv) == 0:
            print("Missing argument 'direction': [0 (open), 1 (close)]")
            return
        direction = int(sys.argv[1])
        if direction != 0 and direction != 1:
            print("Wrong value for argument 'direction': [0 (open), 1 (close)]")
            return
        self.direction = direction
        self.idle = False


if __name__ == '__main__':
    launcher = Launcher()
    launcher.run()
