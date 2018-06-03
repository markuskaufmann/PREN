import logging
import time
from queue import Queue
from threading import Thread
from transitions import Machine, State

from pren36.communicator.Communicator import communicator
from pren36.communicator.CommunicatorEvent import CommunicatorEvent
from pren36.drive.AccelerationMode import AccelerationMode
from pren36.drive.SMFahrwerk import SMFahrwerk
from pren36.drive.SMHub import SMHub
from pren36.endswitch.EndSwitch import EndSwitch
from pren36.fsm.ControllerEvent import ControllerEvent
from pren36.grab.Servomotor import Servomotor
from pren36.lookup.DistanceLookup import DistanceLookup
from pren36.lookup.Locator import Locator
from pren36.serial.IOListener import IOListener

logging.basicConfig(level=logging.INFO)


class StateMachine:
    initialized = False
    dist_x = 0
    dist_z = 0

    # controller
    rec_queue = Queue()
    iolistener = IOListener(rec_queue)
    t_io = None
    t_io_wait = True
    t_stop = None

    # communicator
    communicator = None
    t_comm = None

    # signals
    input_main_start = False
    input_main_stop = False
    input_target_found = False

    # engines
    step_stroke = None
    t_step_stroke = None
    step_drive = None
    t_step_drive = None
    step_drive_wait = True
    step_stroke_wait = True
    servo_grab = None
    t_servo_grab = None
    servo_run = True
    servo_wait = True
    servo_open = False
    servo_close = False

    # sensors
    end_switch = None
    t_end_switch = None
    end_switch_wait = True

    # states
    states = [
        State(name='on'),
        State(name='off'),
        State(name='drive'),
        State(name='stop', on_enter=['smd_stop_driving']),
        State(name='drive_down'),
        State(name='is_down'),
        State(name='get_cube'),
        State(name='drive_up'),
        State(name='set_cube', on_enter=['place_cube']),
        State(name='reach_end', on_enter=['smd_stop_driving'])
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=StateMachine.states, initial='off')

        self.machine.add_transition(trigger='init', source='off', dest='on', after='initialize')
        self.machine.add_transition(trigger='ready_to_drive', source='on', dest='drive',
                                    before='receive_start_signal', after='receive_cube')
        self.machine.add_transition(trigger='cube_found', source='drive', dest='stop', after='open_grabber_woc')
        self.machine.add_transition(trigger='go_down_woc', source='stop', dest='drive_down',
                                    after='drive_to_ground_woc')
        self.machine.add_transition(trigger='reached_surface', source='drive_down', dest='is_down',
                                    after='on_the_ground_woc')
        self.machine.add_transition(trigger='get_cube', source='is_down', dest='get_cube', after='close_grabber_wc')
        self.machine.add_transition(trigger='has_cube', source='get_cube', dest='drive_up', before='start_location',
                                    after='drive_up_wc')
        self.machine.add_transition(trigger='is_up_wc', source='drive_up', dest='drive', before='sms_stop_driving',
                                    after='find_target')
        self.machine.add_transition(trigger='target_area_found', source='drive', dest='stop')
        self.machine.add_transition(trigger='go_down_wc', source='stop', dest='drive_down',
                                    before='adjust_target_location', after='drive_to_ground_wc')
        self.machine.add_transition(trigger='reached_surface', source='drive_down', dest='is_down',
                                    after='on_the_ground_wc')
        self.machine.add_transition(trigger='set_cube', source='is_down', dest='set_cube')
        self.machine.add_transition(trigger='cube_is_set', source='set_cube', dest='drive_up', before='stop_location',
                                    after='drive_up_woc')
        self.machine.add_transition(trigger='is_up_woc', source='drive_up', dest='drive', after='wait_for_touch')
        self.machine.add_transition(trigger='touched_end', source='drive', dest='reach_end', after='finish')
        self.machine.add_transition(trigger='reset', source='reach_end', dest='on', before='clean_up',
                                    after='initialize')

        # emergency stop transitions
        self.machine.add_transition(trigger='emergency_stop', source='drive', dest='stop')
        self.machine.add_transition(trigger='emergency_stop', source='drive_down', dest='stop')
        self.machine.add_transition(trigger='emergency_stop', source='is_down', dest='stop')
        self.machine.add_transition(trigger='emergency_stop', source='get_cube', dest='stop')
        self.machine.add_transition(trigger='emergency_stop', source='drive_up', dest='stop')
        self.machine.add_transition(trigger='emergency_stop', source='set_cube', dest='stop')
        self.machine.add_transition(trigger='emergency_stop', source='reach_end', dest='stop')
        self.machine.add_transition(trigger='reset_after_stop', source='stop', dest='on', after='initialize')

    def initialize(self):
        if not self.initialized:
            self.initialized = True
            self.iolistener.start_idle()

            # communicator
            self.communicator = communicator
            self.communicator.set_fsm(self)
            self.t_comm = Thread(target=self.communicator.run, name="FSM_Communicator")
            self.t_comm.start()
            self.communicator.update_state("INITIALIZE")

            # controller
            self.t_io = Thread(target=self.wait, name="FSM_IOListener_Wait")
            self.t_io.start()
            self.t_stop = Thread(target=self.receive_stop_signal, name="FSM_Controller_Stop_Wait")
            self.t_stop.start()

            # engines
            self.step_stroke = SMHub(SMHub.CCW)
            self.step_drive = SMFahrwerk(SMFahrwerk.CW)
            self.servo_grab = Servomotor()
            self.t_servo_grab = Thread(target=self.servo_control)
            self.t_servo_grab.start()

            # sensors
            self.end_switch = EndSwitch()
            self.t_end_switch = Thread(target=self.end_switch_control)
            self.t_end_switch.start()

        # signals
        self.input_main_start = False
        self.input_main_stop = False
        self.input_target_found = False

        Locator.reset()

        self.communicator.update_state("READY")
        self.ready_to_drive()

    def servo_control(self):
        self.servo_grab.initialize()
        while self.servo_run:
            while self.servo_wait:
                time.sleep(0.02)
            if self.servo_open:
                self.servo_grab.open()
            elif self.servo_close:
                self.servo_grab.close()
            self.servo_wait = True
            self.servo_open = False
            self.servo_close = False
        self.servo_grab.stop()

    def end_switch_control(self):
        while True:
            while self.end_switch_wait:
                time.sleep(0.02)
            while not self.end_switch_wait:
                signal = self.end_switch.signal()
                if signal == 1:
                    self.end_switch_wait = True
                    self.step_drive.request_stop()
                    self.communicator.update_state("RESPONSE_PROCESS STOPPED")
                    self.touched_end()
                time.sleep(0.02)

    def receive_start_signal(self):
        while not self.input_main_start:
            time.sleep(0.02)
        self.communicator.update_state("RESPONSE_PROCESS STARTED")

    def receive_stop_signal(self):
        while True:
            while not self.input_main_stop:
                time.sleep(0.02)
            self.input_main_stop = False
            event_args = ControllerEvent.event_args_main_stop
            event = ControllerEvent(event_args)
            self.notify_controller(event)
            self.communicator.update_state("RESPONSE_PROCESS STOPPED")
            self.emergency_stop()
            self.reset_after_stop()

    def smd_stop_driving(self):
        self.step_drive.request_stop()

    def sms_stop_driving(self):
        self.step_stroke.request_stop()

    def receive_cube(self):
        self.communicator.update_state("GET CUBE")
        distance = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_TO_CUBE]
        self.step_drive.move_distance(distance, AccelerationMode.MODE_START, self.step_drive_callback)
        while self.step_drive_wait:
            time.sleep(0.02)
        self.step_drive_wait = True
        time.sleep(0.5)
        self.cube_found()

    def open_grabber(self):
        self.servo_open = True
        self.servo_wait = False

    def close_grabber(self):
        self.servo_close = True
        self.servo_wait = False

    def open_grabber_woc(self):
        self.open_grabber()
        time.sleep(1)
        self.go_down_woc()

    def close_grabber_wc(self):
        self.close_grabber()
        time.sleep(1)
        self.communicator.update_state("CUBE RECEIVED")
        self.has_cube()

    def place_cube(self):
        self.open_grabber()
        time.sleep(1)
        self.communicator.update_state("CUBE PLACED")
        self.cube_is_set()

    def drive_to_ground_woc(self):
        distance = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_HEIGHT_CUBE]
        self.drive_to_ground(distance)

    def drive_to_ground_wc(self):
        self.communicator.update_state("SET CUBE")
        distance = Locator.z - DistanceLookup.get_delta(Locator.horizontal_x) - \
                   DistanceLookup.DISTANCE_MAP[DistanceLookup.HEIGHT_TARGET_AREA] - 20
        self.drive_to_ground(distance)

    def drive_to_ground(self, distance_mm):
        self.step_stroke.move_distance(distance_mm, SMHub.CCW, self.step_stroke_callback)
        while self.step_stroke_wait:
            time.sleep(0.02)
        self.step_stroke_wait = True
        time.sleep(0.5)
        self.reached_surface()

    def wait_for_touch(self):
        acc_mode = AccelerationMode.determine_acc_mode(Locator.x)
        self.step_drive.move_continuous(acc_mode)
        self.end_switch_wait = False
        threshold = DistanceLookup.DISTANCE_MAP[DistanceLookup.THRESHOLD_SLOW_END]
        while Locator.horizontal_x < threshold:
            time.sleep(0.02)
        self.step_drive.slow_end = True

    def on_the_ground_woc(self):
        self.step_stroke.request_stop()
        self.get_cube()

    def on_the_ground_wc(self):
        self.step_stroke.request_stop()
        self.set_cube()

    def drive_up_woc(self):
        distance = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_HEIGHT_ABOVE_GROUND]
        self.step_stroke.move_distance(distance, SMHub.CW, self.step_stroke_callback)
        while self.step_stroke_wait:
            time.sleep(0.02)
        self.step_stroke_wait = True
        time.sleep(0.5)
        self.is_up_woc()

    def drive_up_wc(self):
        distance = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_HEIGHT_ABOVE_GROUND]
        self.step_stroke.move_distance(distance, SMHub.CW, self.step_stroke_callback)
        while self.step_stroke_wait:
            time.sleep(0.02)
        self.step_stroke_wait = True
        time.sleep(0.5)
        self.is_up_wc()

    def finish(self):
        self.reset()

    def find_target(self):
        self.step_drive.move_continuous(AccelerationMode.MODE_START)
        event_args = ControllerEvent.event_args_improc_start
        event = ControllerEvent(event_args)
        self.notify_controller(event)
        self.communicator.update_state("START IMPROC")
        while not self.input_target_found:
            time.sleep(0.02)
        self.communicator.update_state("TARGET AREA FOUND")
        self.step_drive.request_stop()
        time.sleep(0.5)
        distance = DistanceLookup.DISTANCE_MAP[DistanceLookup.CENTER_ROLL_TO_CAMERA]
        acc_mode = AccelerationMode.determine_acc_mode(Locator.x)
        self.step_drive.move_distance(distance, acc_mode, self.step_drive_callback)
        while self.step_drive_wait:
            time.sleep(0.02)
        time.sleep(0.5)
        self.step_drive_wait = True
        self.step_drive.request_stop()
        self.target_area_found()
        self.go_down_wc()

    def start_location(self):
        Locator.cube_loc = True

    def stop_location(self):
        Locator.cube_loc = False

    def adjust_target_location(self):
        pass

    def clean_up(self):
        pass

    def notify_controller(self, event):
        self.iolistener.send_data_to_output(event)

    def wait(self):
        while self.t_io_wait:
            data = self.rec_queue.get()
            data = str(data).strip()
            if len(data) == 0:
                continue
            print("RECEIVED " + data)
            data = int(data)
            if data == ControllerEvent.event_args_improc_target_found:
                self.input_target_found = True

    def comm_callback(self, event):
        data = event.args
        if data == CommunicatorEvent.event_args_start:
            self.input_main_start = True
        elif data == CommunicatorEvent.event_args_stop:
            self.input_main_stop = True

    def step_drive_callback(self):
        self.step_drive_wait = False

    def step_stroke_callback(self):
        self.step_stroke_wait = False
