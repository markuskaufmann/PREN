import sys
import time
from threading import Thread

from pren36.drive.AccelerationMode import AccelerationMode
from pren36.drive.SMFahrwerk import SMFahrwerk
from pren36.drive.SMHub import SMHub
from pren36.grab.Servomotor import Servomotor
from pren36.lookup.DistanceLookup import DistanceLookup


class Launcher:
    step_drive = None
    step_drive_wait = True
    step_stroke = None
    step_stroke_wait = True
    grabber = None
    conn = None

    def __init__(self):
        DistanceLookup.init_dict()
        self.step_drive = SMFahrwerk(SMFahrwerk.CW)
        self.step_stroke = SMHub(SMHub.CW)
        self.grabber = Servomotor()
        self.idle = True
        t_fsm = Thread(target=self.start_idle)
        t_fsm.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        try:
            self.grabber.initialize()
            time.sleep(3)
            distance = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_TO_CUBE]
            self.step_drive.move_distance(distance, AccelerationMode.MODE_START, self.step_drive_callback)
            while self.step_drive_wait:
                time.sleep(0.02)
            self.step_drive_wait = True
            distance = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_HEIGHT_CUBE]
            print("height: " + str(distance))
            self.step_stroke.move_distance(distance, SMHub.CCW, self.step_stroke_callback)
            while self.step_stroke_wait:
                time.sleep(0.02)
            self.step_stroke_wait = True
            time.sleep(1)
            self.grabber.close()
            time.sleep(1)
            self.step_stroke.move_distance(distance, SMHub.CW, self.step_stroke_callback)
            while self.step_stroke_wait:
                time.sleep(0.02)
            time.sleep(1)
            self.step_stroke_wait = True
            self.step_drive.move_continuous(AccelerationMode.MODE_START)
            self.grabber.stop()
            return
        except KeyboardInterrupt:
            self.step_drive.request_stop()
            self.step_stroke.request_stop()
            self.grabber.stop()
            sys.exit()

    def step_drive_callback(self):
        self.step_drive_wait = False

    def step_stroke_callback(self):
        self.step_stroke_wait = False

    def run(self):
        self.idle = False


if __name__ == '__main__':
    launcher = Launcher()
    launcher.run()
