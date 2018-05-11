import logging
import time
from threading import Thread
from multiprocessing import Process, Pipe
from transitions import Machine, State

from ch.hslu.pren36.pi3b.endswitch.EndSwitch import EndSwitch
from ch.hslu.pren36.pi3b.main.Controller import Controller
from ch.hslu.pren36.pi3b.main.ControllerEvent import ControllerEvent
from ch.hslu.pren36.pi3b.servomotor.Servomotor import Servomotor
from ch.hslu.pren36.pi3b.stepmotor.Stepmotor import StepMotor
from ch.hslu.pren36.pi3b.stepmotorFahrwerk.StepmotorFahrwerk import StepmotorFahrwerk
from ch.hslu.pren36.pi3b.tof.TOFSensor import TOFSensor
from ch.hslu.pren36.pi3b.ultrasound.UltrasoundSensor import UltraSoundSensor

logging.basicConfig(level=logging.INFO)
# logging.getLogger('transitions').setLevel(logging.INFO)


class StateMachine:
    initialized = False
    dist_x = 0
    dist_z = 0

    # controller
    controller = Controller()
    proc_controller = None
    conn_controller_parent, conn_controller_child = Pipe(duplex=True)
    t_controller = None
    t_controller_wait = True
    t_stop = None

    # signals
    input_main_start = False
    input_main_stop = False
    input_target_found = False

    # engines
    step_stroke = None
    t_step_stroke = None
    step_drive = None
    t_step_drive = None
    servo_grab = None
    t_servo_grab = None
    servo_run = True
    servo_wait = True
    servo_open = False
    servo_close = False

    # sensors
    ultrasound = None
    t_ultrasound = None
    ultrasound_wait = True
    tof = None
    t_tof = None
    tof_wait = True
    end_switch = None
    t_end_switch = None
    end_switch_wait = True

    # states
    states = [
        State(name='on'),
        State(name='off'),
        State(name='drive', on_enter=['smd_drive_forward']),
        State(name='stop', on_enter=['smd_stop_driving']),
        State(name='drive_down', on_enter=['sms_drive_down']),
        State(name='is_down', on_enter=['sms_stop_driving']),
        State(name='get_cube'),
        State(name='drive_up', on_enter=['sms_drive_up']),
        State(name='set_cube', on_enter=['place_cube']),
        State(name='reach_end', on_enter=['smd_stop_driving'])
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=StateMachine.states, initial='off')

        self.machine.add_transition(trigger='init', source='off', dest='on', after='initialize')
        self.machine.add_transition(trigger='ready_to_drive', source='on', dest='drive',
                                    before='receive_start_signal', after='stop_for_cube')
        self.machine.add_transition(trigger='cube_found', source='drive', dest='stop', after='open_grabber')
        self.machine.add_transition(trigger='go_down_woc', source='stop', dest='drive_down', after='simulate_ground')
        self.machine.add_transition(trigger='reached_surface', source='drive_down', dest='is_down',
                                    after='on_the_ground_woc')
        self.machine.add_transition(trigger='get_cube', source='is_down', dest='get_cube', after='close_grabber_wc')
        self.machine.add_transition(trigger='has_cube', source='get_cube', dest='drive_up', before='start_location',
                                    after='on_the_top_wc')
        self.machine.add_transition(trigger='is_up_wc', source='drive_up', dest='drive', before='sms_stop_driving',
                                    after='find_target')
        self.machine.add_transition(trigger='target_area_found', source='drive', dest='stop')
        self.machine.add_transition(trigger='go_down_wc', source='stop', dest='drive_down',
                                    before='adjust_target_location', after='simulate_ground')
        self.machine.add_transition(trigger='reached_surface', source='drive_down', dest='is_down',
                                    after='on_the_ground_wc')
        self.machine.add_transition(trigger='set_cube', source='is_down', dest='set_cube')
        self.machine.add_transition(trigger='cube_is_set', source='set_cube', dest='drive_up', before='stop_location',
                                    after='on_the_top_woc')
        self.machine.add_transition(trigger='is_up_woc', source='drive_up', dest='drive', before='close_grabber',
                                    after='wait_for_touch')
        self.machine.add_transition(trigger='touched_end', source='drive', dest='reach_end', after='finish')
        self.machine.add_transition(trigger='shut_down', source='reach_end', dest='off', before='clean_up')

        # emergency stop transitions
        self.machine.add_transition(trigger='emergency_stop', source='drive', dest='stop')
        self.machine.add_transition(trigger='emergency_stop', source='drive_while_waiting', dest='stop')
        self.machine.add_transition(trigger='emergency_stop', source='drive_down', dest='stop')
        self.machine.add_transition(trigger='emergency_stop', source='is_down', dest='stop')
        self.machine.add_transition(trigger='emergency_stop', source='get_cube', dest='stop')
        self.machine.add_transition(trigger='emergency_stop', source='drive_up', dest='stop')
        self.machine.add_transition(trigger='emergency_stop', source='set_cube', dest='stop')
        self.machine.add_transition(trigger='emergency_stop', source='reach_end', dest='stop')
        self.machine.add_transition(trigger='reset_after_stop', source='stop', dest='on')

    def initialize(self):
        if not self.initialized:
            self.initialized = True

            # signals
            self.input_main_start = False
            self.input_main_stop = False
            self.input_target_found = False

            # controller
            self.proc_controller = Process(target=self.controller.start, name="FSM_Controller",
                                           args=(self.conn_controller_child,))
            self.proc_controller.start()
            self.t_controller = Thread(target=self.wait, name="FSM_Controller_Wait")
            self.t_controller.start()
            self.t_stop = Thread(target=self.receive_stop_signal, name="FSM_Controller_Stop_Wait")
            self.t_stop.start()

            # engines
            self.step_stroke = StepMotor(StepMotor.CW)
            self.t_step_stroke = Thread(target=self.step_stroke.control)
            self.t_step_stroke.start()
            self.step_drive = StepmotorFahrwerk(StepmotorFahrwerk.CW)
            self.t_step_drive = Thread(target=self.step_drive.control)
            self.t_step_drive.start()
            self.servo_grab = Servomotor()
            self.t_servo_grab = Thread(target=self.servo_control)
            self.t_servo_grab.start()

            # sensors
            self.ultrasound = UltraSoundSensor()
            self.t_ultrasound = Thread(target=self.ultrasound_control)
            self.t_ultrasound.start()
            self.tof = TOFSensor()
            self.t_tof = Thread(target=self.tof_control)
            self.t_tof.start()
            self.end_switch = EndSwitch()
            self.t_end_switch = Thread(target=self.end_switch_control)
            self.t_end_switch.start()

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

    def ultrasound_control(self):
        while self.ultrasound_wait:
            time.sleep(0.02)
        while not self.ultrasound_wait:
            self.dist_x = self.ultrasound.distance()
            print(self.dist_x)
            time.sleep(0.5)

    def tof_control(self):
        while self.tof_wait:
            time.sleep(0.02)
        while not self.tof_wait:
            self.dist_z = self.tof.distance()
            print(self.dist_z)
            time.sleep(0.5)

    def end_switch_control(self):
        while True:
            while self.end_switch_wait:
                time.sleep(0.02)
            while not self.end_switch_wait:
                signal = self.end_switch.signal()
                if signal == 1:
                    self.end_switch_wait = True
                    self.touched_end()
                time.sleep(0.2)

    def receive_start_signal(self):
        while not self.input_main_start:
            time.sleep(0.02)
        event_args = ControllerEvent.event_args_main_start
        event = ControllerEvent(event_args)
        self.notify_controller(event)

    def receive_stop_signal(self):
        while not self.input_main_stop:
            time.sleep(0.02)
        event_args = ControllerEvent.event_args_main_stop
        event = ControllerEvent(event_args)
        self.notify_controller(event)
        self.emergency_stop()
        self.reset_after_stop()

    def smd_drive_forward(self):
        self.step_drive.set_direction(StepmotorFahrwerk.CCW)
        self.step_drive.set_state(StepmotorFahrwerk.state['acc'])

    def smd_stop_driving(self):
        self.step_drive.set_state(StepmotorFahrwerk.state['stop'])

    def sms_drive_down(self):
        self.step_stroke.set_direction(StepmotorFahrwerk.CW)
        self.step_stroke.set_state(StepmotorFahrwerk.state['acc'])

    def sms_drive_up(self):
        self.step_stroke.set_direction(StepmotorFahrwerk.CCW)
        self.step_stroke.set_state(StepmotorFahrwerk.state['acc'])

    def sms_stop_driving(self):
        self.step_stroke.set_state(StepmotorFahrwerk.state['stop'])

    def stop_for_cube(self):
        time.sleep(3)
        self.cube_found()

    def open_grabber(self):
        self.servo_open = True
        self.servo_wait = False
        self.go_down_woc()

    def close_grabber(self):
        self.servo_close = True
        self.servo_wait = False

    def close_grabber_wc(self):
        self.close_grabber()
        self.has_cube()

    def place_cube(self):
        self.servo_open = True
        self.servo_wait = False
        self.cube_is_set()

    def simulate_ground(self):
        time.sleep(3)
        self.reached_surface()

    def wait_for_touch(self):
        self.end_switch_wait = False

    def on_the_ground_woc(self):
        self.get_cube()

    def on_the_ground_wc(self):
        self.set_cube()

    def on_the_top_woc(self):
        time.sleep(3)
        self.is_up_woc()

    def on_the_top_wc(self):
        time.sleep(3)
        self.is_up_wc()

    def finish(self):
        self.shut_down()

    def find_target(self):
        event_args = ControllerEvent.event_args_improc_start
        event = ControllerEvent(event_args)
        self.notify_controller(event)
        while not self.input_target_found:
            time.sleep(0.02)
        print("Target area found")
        self.target_area_found()
        self.go_down_wc()

    def start_location(self):
        self.ultrasound_wait = False
        self.tof_wait = False

    def stop_location(self):
        self.ultrasound_wait = True
        self.tof_wait = True

    def adjust_target_location(self):
        pass

    def clean_up(self):
        pass

    def notify_controller(self, event):
        self.conn_controller_parent.send(event)

    def wait(self):
        while self.t_controller_wait:
            controller_event = self.conn_controller_parent.recv()
            if controller_event.args == ControllerEvent.event_args_main_start:
                self.input_main_start = True
            elif controller_event.args == ControllerEvent.event_args_main_stop:
                self.input_main_stop = True
            elif controller_event.args == ControllerEvent.event_args_improc_target_found:
                self.input_target_found = True
