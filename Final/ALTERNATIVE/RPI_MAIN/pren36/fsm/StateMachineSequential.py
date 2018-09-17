import time
from multiprocessing import Process
from queue import Queue
from threading import Thread

from pren36.communicator.CommObject import CommObject
from pren36.communicator.Communicator import communicator
from pren36.drive.AccelerationMode import AccelerationMode
from pren36.drive.SMFahrwerkNonThreaded import SMFahrwerk
from pren36.drive.SMHubNonThreaded import SMHub
from pren36.endswitch.EndSwitch import EndSwitch
from pren36.fsm.ControllerEvent import ControllerEvent
from pren36.grab.Servomotor import Servomotor
from pren36.lookup.DistanceLookup import DistanceLookup
from pren36.lookup.Locator import Locator
from pren36.serial.IOListener import IOListener


class StateMachine:
    initialized = False
    current_state = None

    # controller
    rec_queue = Queue()
    iolistener = IOListener(rec_queue)
    t_io = None
    t_io_wait = True
    t_stop = None

    # signals
    input_start = False
    input_stop = False
    input_target_found = False
    height_response = 0

    # engines
    step_stroke = None
    step_drive = None
    servo_grab = None

    # sensors
    end_switch = None
    t_end_switch = None
    end_switch_wait = True

    # location
    t_loc = None
    t_location = False

    # states
    # states = [
    #     State(name='on'),
    #     State(name='off'),
    #     State(name='drive'),
    #     State(name='stop', on_enter=['smd_stop_driving', 'sms_stop_driving']),
    #     State(name='drive_down'),
    #     State(name='is_down'),
    #     State(name='get_cube'),
    #     State(name='drive_up'),
    #     State(name='set_cube', on_enter=['place_cube']),
    #     State(name='reach_end', on_enter=['smd_stop_driving'])
    # ]

    def __init__(self):
        # self.machine = Machine(model=self, states=StateMachine.states, initial='off')
        #
        # self.machine.add_transition(trigger='init', source='off', dest='on', after='initialize')
        # self.machine.add_transition(trigger='ready_to_drive', source='on', dest='drive',
        #                             before='receive_start_signal', after='receive_cube')
        # self.machine.add_transition(trigger='cube_found', source='drive', dest='stop', after='open_grabber_woc')
        # self.machine.add_transition(trigger='go_down_woc', source='stop', dest='drive_down',
        #                             after='drive_to_ground_woc')
        # self.machine.add_transition(trigger='reached_surface', source='drive_down', dest='is_down',
        #                             after='on_the_ground_woc')
        # self.machine.add_transition(trigger='get_cube', source='is_down', dest='get_cube', after='close_grabber_wc')
        # self.machine.add_transition(trigger='has_cube', source='get_cube', dest='drive_up', before='start_location',
        #                             after='drive_up_wc')
        # self.machine.add_transition(trigger='is_up_wc', source='drive_up', dest='drive', before='sms_stop_driving',
        #                             after='find_target')
        # self.machine.add_transition(trigger='target_area_found', source='drive', dest='stop')
        # self.machine.add_transition(trigger='go_down_wc', source='stop', dest='drive_down',
        #                             before='adjust_target_location', after='drive_to_ground_wc')
        # self.machine.add_transition(trigger='reached_surface', source='drive_down', dest='is_down',
        #                             after='on_the_ground_wc')
        # self.machine.add_transition(trigger='set_cube', source='is_down', dest='set_cube')
        # self.machine.add_transition(trigger='cube_is_set', source='set_cube', dest='drive_up', before='stop_location',
        #                             after='drive_up_woc')
        # self.machine.add_transition(trigger='is_up_woc', source='drive_up', dest='drive', after='wait_for_touch')
        # self.machine.add_transition(trigger='touched_end', source='drive', dest='reach_end', after='finish')
        # self.machine.add_transition(trigger='reset', source='reach_end', dest='on', before='clean_up',
        #                             after='initialize')
        #
        # # emergency stop transitions
        # self.machine.add_transition(trigger='emergency_stop', source='drive', dest='stop')
        # self.machine.add_transition(trigger='emergency_stop', source='drive_down', dest='stop')
        # self.machine.add_transition(trigger='emergency_stop', source='is_down', dest='stop')
        # self.machine.add_transition(trigger='emergency_stop', source='get_cube', dest='stop')
        # self.machine.add_transition(trigger='emergency_stop', source='drive_up', dest='stop')
        # self.machine.add_transition(trigger='emergency_stop', source='set_cube', dest='stop')
        # self.machine.add_transition(trigger='emergency_stop', source='reach_end', dest='stop')
        # self.machine.add_transition(trigger='reset_after_stop', source='stop', dest='on', after='initialize')
        pass

    def initialize(self):
        if not self.initialized:
            self.initialized = True
            self.iolistener.start_idle()

            # DistanceLookup
            DistanceLookup.init_dict()

            # controller
            self.t_io = Thread(target=self.wait, name="FSM_IOListener_Wait")
            self.t_io.start()
            self.t_stop = Thread(target=self.receive_stop_signal, name="FSM_Controller_Stop_Wait")
            self.t_stop.start()

            # engines
            self.step_stroke = SMHub(SMHub.CCW)
            self.step_drive = SMFahrwerk(SMFahrwerk.CW)
            self.servo_grab = Servomotor()

            # sensors
            self.end_switch = EndSwitch()
            self.t_end_switch = Thread(target=self.end_switch_control)

            # location
            self.t_loc = Thread(target=self.location)
            self.t_loc.start()

        # signals
        self.input_start = False
        self.input_stop = False
        self.input_target_found = False
        self.height_response = 0

        Locator.reset()

        self.update_state("READY")
        self.receive_start_signal()

    def update_state(self, new_state):
        self.current_state = new_state

    def end_switch_control(self):
        while True:
            while self.end_switch_wait:
                time.sleep(0.05)
            while not self.end_switch_wait:
                signal = self.end_switch.signal()
                if signal == 1:
                    self.end_switch_wait = True
                    self.update_state("RESPONSE_PROCESS STOPPED")
                    self.smd_stop_driving()
                    self.sms_stop_driving()
                    time.sleep(0.5)
                    self.t_location = False
                    self.notify_controller(ControllerEvent(ControllerEvent.event_args_main_finish))
                    self.finish()
                time.sleep(0.2)

    def receive_start_signal(self):
        while not self.input_start:
            time.sleep(0.02)
        # time.sleep(1)
        self.update_state("RESPONSE_PROCESS STARTED")
        self.receive_cube()

    def receive_stop_signal(self):
        while True:
            while not self.input_stop:
                time.sleep(0.2)
            self.update_state("RESPONSE_PROCESS STOPPED")
            self.smd_stop_driving()
            self.sms_stop_driving()
            time.sleep(0.5)
            self.t_location = False
            self.finish()

    def smd_stop_driving(self):
        self.step_drive.request_stop()

    def sms_stop_driving(self):
        self.step_stroke.request_stop()

    def receive_cube(self):
        self.update_state("GET CUBE")
        distance = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_TO_CUBE]
        self.step_drive.move_distance(distance, AccelerationMode.MODE_START, None)
        self.smd_stop_driving()
        self.sms_stop_driving()
        self.open_grabber_woc()

    def open_grabber(self):
        # self.servo_grab.initialize(0)
        self.servo_grab.open()
        # self.servo_grab.stop()

    def close_grabber(self):
        # self.servo_grab.initialize(0)
        self.servo_grab.close()
        # self.servo_grab.stop()

    def open_grabber_woc(self):
        # self.open_grabber()
        self.drive_to_ground_woc()

    def close_grabber_wc(self):
        self.close_grabber()
        self.update_state("CUBE RECEIVED")
        self.start_location()
        self.drive_up_wc()

    def place_cube(self):
        time.sleep(1)
        Locator.zc = 15
        self.open_grabber()
        self.update_state("CUBE PLACED")
        self.stop_location()
        self.drive_up_woc()

    def drive_to_ground_woc(self):
        distance = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_HEIGHT_CUBE]
        self.step_stroke.move_distance(distance, SMHub.CCW, None)
        self.on_the_ground_woc()

    def drive_to_ground_wc(self):
        self.update_state("SET CUBE")
        while self.height_response == 0:
            time.sleep(0.05)
        distance = self.height_response - DistanceLookup.DISTANCE_MAP[DistanceLookup.HEIGHT_TARGET_AREA] - \
                    DistanceLookup.DISTANCE_MAP[DistanceLookup.HEIGHT_CONS_TO_CUBE] - 10
        self.step_stroke.move_distance(distance, SMHub.CCW, None)
        self.on_the_ground_wc()

    def wait_for_touch(self):
        self.t_end_switch.start()
        acc_mode = AccelerationMode.determine_acc_mode(Locator.x)
        self.end_switch_wait = False
        self.step_drive.move_continuous(acc_mode)

    def on_the_ground_woc(self):
        self.step_stroke.request_stop()
        self.close_grabber_wc()

    def on_the_ground_wc(self):
        self.step_stroke.request_stop()
        self.place_cube()

    def drive_up_woc(self):
        distance = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_HEIGHT_ABOVE_GROUND]
        self.step_stroke.move_distance(distance, SMHub.CW, None)
        self.wait_for_touch()

    def drive_up_wc(self):
        distance = DistanceLookup.DISTANCE_MAP[DistanceLookup.START_HEIGHT_ABOVE_GROUND]
        self.step_stroke.move_distance(distance, SMHub.CW, None)
        self.sms_stop_driving()
        self.find_target()

    def finish(self):
        self.clean_up()
        self.initialize()

    def find_target(self):
        move_start = False
        while not self.input_target_found:
            if not move_start:
                move_start = True
                event_args = ControllerEvent.event_args_improc_start
                event = ControllerEvent(event_args)
                self.notify_controller(event)
                self.update_state("START IMPROC")
                self.step_drive.move_continuous(AccelerationMode.MODE_START)
            time.sleep(0.5)
        self.update_state("TARGET AREA FOUND")
        # distance = DistanceLookup.DISTANCE_MAP[DistanceLookup.CENTER_ROLL_TO_CAMERA]
        # acc_mode = AccelerationMode.determine_acc_mode(Locator.x)
        # self.step_drive.move_distance(distance, acc_mode, None)
        self.smd_stop_driving()
        self.sms_stop_driving()
        event = ControllerEvent(ControllerEvent.event_args_req_height)
        self.notify_controller(event)
        self.adjust_target_location()
        self.drive_to_ground_wc()

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
            if data == str(ControllerEvent.event_args_improc_target_found):
                self.input_target_found = True
                time.sleep(0.52)
                self.smd_stop_driving()
            elif data == str(ControllerEvent.event_args_main_start):
                self.input_start = True
                self.t_location = True
            elif data == str(ControllerEvent.event_args_main_stop):
                self.input_stop = True
                self.t_location = False
            else:
                self.height_response = float(data)

    def location(self):
        while True:
            if self.t_location:
                event = ControllerEvent(self.current_state + ";" + Locator.loc_cube())
                self.notify_controller(event)
            time.sleep(0.5)
