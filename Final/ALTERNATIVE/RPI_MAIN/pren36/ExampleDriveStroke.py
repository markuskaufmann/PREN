import sys
import time
from threading import Thread

from pren36.drive.SMHub import SMHub
from pren36.lookup.DistanceLookup import DistanceLookup


class Launcher:
    step_stroke = None
    step_stroke_wait = True

    direction = None
    distance = None

    def __init__(self):
        DistanceLookup.init_dict()
        self.step_stroke = SMHub(SMHub.CCW)
        self.idle = True
        t_fsm = Thread(target=self.start_idle)
        t_fsm.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        try:
            self.step_stroke.move_distance(self.distance, self.direction, self.step_stroke_callback)
            while self.step_stroke_wait:
                time.sleep(0.02)
            time.sleep(1)
            self.step_stroke_wait = True
        except KeyboardInterrupt:
            self.step_stroke.request_stop()
            sys.exit()

    def step_stroke_callback(self):
        self.step_stroke_wait = False

    def run(self):
        if len(sys.argv) == 0:
            print("Missing argument 'direction': [cw=1 (up), ccw=0 (down)]")
            print("Missing argument 'distance': [int, mm, > 0]")
            return
        direction = int(sys.argv[1])
        if direction != 0 and direction != 1:
            print("Wrong value for argument 'direction': [cw=1 (up), ccw=0 (down)]")
            return
        distance = int(sys.argv[2])
        if distance == 0:
            print("Wrong value for argument 'distance': [int, mm, > 0]")
            return
        self.direction = direction
        self.distance = distance
        self.idle = False


if __name__ == '__main__':
    launcher = Launcher()
    launcher.run()
