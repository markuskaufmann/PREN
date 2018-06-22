import sys
import time
from threading import Thread

from pren36.drive.AccelerationMode import AccelerationMode
from pren36.drive.SMFahrwerk import SMFahrwerk
from pren36.lookup.DistanceLookup import DistanceLookup


class Launcher:
    step_drive = None
    step_drive_wait = True

    direction = None

    def __init__(self):
        DistanceLookup.init_dict()
        self.step_drive = SMFahrwerk(SMFahrwerk.CW)
        self.idle = True
        t_fsm = Thread(target=self.start_idle)
        t_fsm.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        try:
            self.step_drive.set_direction(self.direction)
            self.step_drive.move_continuous(AccelerationMode.MODE_START)
        except KeyboardInterrupt:
            self.step_drive.request_stop()
            sys.exit()

    def run(self):
        if len(sys.argv) == 0:
            print("Missing argument 'direction': [cw=1 (up), ccw=0 (down)]")
            return
        direction = int(sys.argv[1])
        if direction != 0 and direction != 1:
            print("Wrong value for argument 'direction': [cw=1 (up), ccw=0 (down)]")
            return
        self.direction = direction
        self.idle = False


if __name__ == '__main__':
    launcher = Launcher()
    launcher.run()
