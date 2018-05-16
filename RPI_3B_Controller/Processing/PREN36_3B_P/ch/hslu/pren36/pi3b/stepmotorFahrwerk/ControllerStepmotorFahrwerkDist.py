import sys
import time
from threading import Thread

from ch.hslu.pren36.pi3b.lookup.Locator import Locator
from ch.hslu.pren36.pi3b.stepmotorFahrwerk.AccMode import AccMode
from ch.hslu.pren36.pi3b.stepmotorFahrwerk.StepmotorFahrwerkDist import StepmotorFahrwerk


class ControllerStepmotorFahrwerkDist:
    sm = None
    t_sm = None
    t_loc = None

    def __init__(self):
        self.sm = StepmotorFahrwerk(1)
        self.t_sm = Thread(target=self.sm.control)
        self.t_sm.start()
        self.t_loc = Thread(target=self.print_loc)
        self.t_loc.start()
        self.print = True

    def move_distance(self, distance_mm):
        try:
            if distance_mm > 0:
                self.sm.move_distance(distance_mm, AccMode.MODE_START)
            elif distance_mm == -1:
                self.sm.move_continuous(AccMode.MODE_START)
        except KeyboardInterrupt:
            self.print = False
            self.sm.set_state(StepmotorFahrwerk.STATE_STOP)

    def print_loc(self):
        while self.print:
            print(Locator.loc())
            time.sleep(0.5)


def start():
    if len(sys.argv) == 0:
        print("Missing argument 'distance': [int, mm, > 0]")
        return
    distance = int(sys.argv[1])
    if distance == 0:
        print("Wrong value for argument 'distance': [int, mm, > 0]")
        return
    csm = ControllerStepmotorFahrwerkDist()
    csm.move_distance(distance)


if __name__ == '__main__':
    start()
