import sys
import time
from threading import Thread

from pren36.drive.AccelerationMode import AccelerationMode
from pren36.drive.SMFahrwerk import SMFahrwerk
from pren36.lookup.Locator import Locator


class Launcher:
    step_drive = None
    step_drive_wait = True

    direction = None
    distance = None

    def __init__(self):
        self.step_drive = SMFahrwerk(SMFahrwerk.CW)
        self.idle = True
        t_fsm = Thread(target=self.start_idle)
        t_fsm.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        try:
            print("height: " + str(Locator.z))
            self.step_drive.set_direction(self.direction)
            self.step_drive.move_distance(self.distance, AccelerationMode.MODE_START, self.step_drive_callback)
            while self.step_drive_wait:
                time.sleep(0.02)
            time.sleep(1)
            self.step_drive_wait = True
            print("height: " + str(Locator.z))
        except KeyboardInterrupt:
            self.step_drive.request_stop()
            sys.exit()

    def step_drive_callback(self):
        self.step_drive_wait = False

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
