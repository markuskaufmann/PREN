import sys
import time
from threading import Thread

from ch.hslu.pren36.pi3b.stepmotor.StepmotorDist import Stepmotor


class ControllerStepmotorDist:
    sm = None
    t_sm = None

    def __init__(self):
        self.sm = Stepmotor(1)
        self.t_sm = Thread(target=self.sm.control)
        self.t_sm.start()

    def move_distance(self, distance_cm, direction):
        try:
            if distance_cm > 0:
                self.sm.move_distance(distance_cm, direction)
            elif distance_cm == -1:
                self.sm.move_continuous(direction)
        except KeyboardInterrupt:
            self.sm.set_state(Stepmotor.STATE_STOP)


def start():
    if len(sys.argv) == 0:
        print("Missing argument 'direction': [cw=1 (up), ccw=0 (down)]")
        print("Missing argument 'distance': [int, cm, > 0]")
        return
    direction = int(sys.argv[1])
    if direction != 0 and direction != 1:
        print("Wrong value for argument 'direction': [cw=1 (up), ccw=0 (down)]")
        return
    distance = int(sys.argv[2])
    if distance == 0:
        print("Wrong value for argument 'distance': [int, cm, > 0]")
        return
    csm = ControllerStepmotorDist()
    csm.move_distance(distance, direction)


if __name__ == '__main__':
    start()
