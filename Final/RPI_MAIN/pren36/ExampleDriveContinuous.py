import sys
import time
from threading import Thread

from pren36.drive.AccelerationMode import AccelerationMode
from pren36.drive.SMFahrwerk import SMFahrwerk
from pren36.drive.SMHub import SMHub
from pren36.grab.Servomotor import Servomotor
from pren36.lookup.DistanceLookup import DistanceLookup
from pren36.lookup.Locator import Locator


class Launcher:
    step_drive = None
    step_drive_wait = True

    def __init__(self):
        self.step_drive = SMFahrwerk(SMFahrwerk.CW)
        self.idle = True
        t_fsm = Thread(target=self.start_idle)
        t_fsm.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        try:
            self.step_drive.move_continuous(AccelerationMode.MODE_START)
        except KeyboardInterrupt:
            self.step_drive.request_stop()
            sys.exit()

    def run(self):
        self.idle = False


if __name__ == '__main__':
    launcher = Launcher()
    launcher.run()
