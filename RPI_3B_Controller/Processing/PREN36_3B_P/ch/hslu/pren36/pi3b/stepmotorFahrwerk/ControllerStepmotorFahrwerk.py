import sys
import time
from threading import Thread
from ch.hslu.pren36.pi3b.stepmotorFahrwerk.StepmotorFahrwerk import StepmotorFahrwerk


class ControllerStepmotorFahrwerk:
    idle = True
    running = False
    t_running = None
    t_sm = None
    sm = None

    def __init__(self, direction):
        self.sm = StepmotorFahrwerk(direction)
        self.t_running = Thread(target=self.start_idle)
        self.t_running.start()
        self.t_sm = Thread(target=self.sm.control)
        self.t_sm.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        try:
            time.sleep(1)
            self.sm.set_state(StepmotorFahrwerk.state['acc'])
            while self.running:
                time.sleep(0.02)
        except KeyboardInterrupt:
            self.sm.set_state(StepmotorFahrwerk.state['stop'])
            return

    def run(self):
        self.running = True
        self.idle = False


def start():
    if len(sys.argv) == 0:
        print("Missing argument 'direction': [cw=1, ccw=0]")
        return
    direction = int(sys.argv[1])
    if direction != 0 and direction != 1:
        print("Wrong value for argument 'direction': [cw=1, ccw=0]")
        return
    csm = ControllerStepmotorFahrwerk(direction)
    csm.run()


if __name__ == '__main__':
    start()
