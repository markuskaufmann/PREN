import time
from queue import Queue
from threading import Thread

from pren36.communicator.CommObject import CommObject
from pren36.drive.AccelerationMode import AccelerationMode
from pren36.drive.SMFahrwerkNonThreaded import SMFahrwerk
from pren36.drive.SMHubNonThreaded import SMHub
from pren36.fsm.ControllerEvent import ControllerEvent
from pren36.grab.Servomotor import Servomotor
from pren36.lookup.DistanceLookup import DistanceLookup
from pren36.lookup.Locator import Locator
from pren36.serial.IOListener import IOListener


class ExampleImproc:
    def __init__(self):
        DistanceLookup.init_dict()
        self.comm_object = CommObject()
        Locator.comm_object = self.comm_object
        self.comm_object.reset()
        Locator.reset()
        self.step_drive = SMFahrwerk(SMFahrwerk.CW)
        self.step_stroke = SMHub(SMHub.CW)
        self.rec_queue = Queue()
        self.iolistener = IOListener(self.rec_queue)
        self.t_io = None
        self.t_io_wait = True
        self.iolistener.start_idle()
        self.input_target_found = False
        self.t_io = Thread(target=self.wait, name="FSM_IOListener_Wait")
        self.t_io.start()

    def find_target(self):
        move_start = False
        while not self.input_target_found:
            if not move_start:
                move_start = True
                event_args = ControllerEvent.event_args_improc_start
                event = ControllerEvent(event_args)
                self.iolistener.send_data_to_output(event)
                self.comm_object.update_state("START IMPROC")
                self.step_drive.move_continuous(AccelerationMode.MODE_START)
            time.sleep(0.5)
        self.step_drive.request_stop()
        self.comm_object.update_state("TARGET AREA FOUND")
        time.sleep(0.5)
        distance = DistanceLookup.DISTANCE_MAP[DistanceLookup.CENTER_ROLL_TO_CAMERA]
        acc_mode = AccelerationMode.determine_acc_mode(Locator.x)
        self.step_drive.move_distance(distance, acc_mode, None)
        self.drive_to_ground_wc()

    def drive_to_ground_wc(self):
        self.comm_object.update_state("SET CUBE")
        distance = Locator.z - DistanceLookup.get_delta(Locator.x) - \
                   DistanceLookup.DISTANCE_MAP[DistanceLookup.HEIGHT_TARGET_AREA] - 20
        self.step_stroke.move_distance(distance, SMHub.CCW, None)

    def wait(self):
        while self.t_io_wait:
            data = self.rec_queue.get()
            data = str(data).strip()
            if len(data) == 0:
                continue
            if data == str(ControllerEvent.event_args_improc_target_found):
                print("target found")
                self.input_target_found = True


if __name__ == '__main__':
    ex_improc = ExampleImproc()
    ex_improc.find_target()
