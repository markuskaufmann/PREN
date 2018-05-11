import sys
import time
from threading import Thread

from ch.hslu.pren36.pi3b.stepmotorFahrwerk.AccMode import AccMode
from ch.hslu.pren36.pi3b.stepmotorFahrwerk.StepmotorFahrwerkDist import StepmotorFahrwerk


class ControllerStepmotorFahrwerkDist:
    sm = None
    t_sm = None

    def __init__(self):
        self.sm = StepmotorFahrwerk(1)
        self.t_sm = Thread(target=self.sm.control)
        self.t_sm.start()

    def move_distance(self, distance_cm):
        try:
            if distance_cm > 0:
                self.sm.move_distance(distance_cm, AccMode.MODE_START)
            elif distance_cm == -1:
                self.sm.move_continuous(AccMode.MODE_START)
        except KeyboardInterrupt:
            self.sm.set_state(StepmotorFahrwerk.STATE_STOP)


def start():
    if len(sys.argv) == 0:
        print("Missing argument 'distance': [int, cm, > 0]")
        return
    distance = int(sys.argv[1])
    if distance == 0:
        print("Wrong value for argument 'distance': [int, cm, > 0]")
        return
    csm = ControllerStepmotorFahrwerkDist()
    csm.move_distance(distance)


if __name__ == '__main__':
    start()
