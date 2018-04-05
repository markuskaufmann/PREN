import time
from threading import Thread
from ch.hslu.pren36.pi3b.io.SimSerialConnection import SimSerialConnection
# from ch.hslu.pren36.pi3b.io.SerialConnection import SerialConnection
from ch.hslu.pren36.pi3b.main.ControllerEvent import ControllerEvent


class IOListener:
    proc_conn = None
    t_wait = None
    t_wait_running = True
    t_listen_state = None
    t_listen_loc = None
    serial_conn = SimSerialConnection()
    output_start = "start"
    output_stop = "stop"
    output_improc = "improc_found"
    input_improc = "improc_launch"
    input_loc = "loc"
    input_finish = "finish"
    existing = True
    idle = True
    running = False

    def start_idle(self, conn):
        self.proc_conn = conn
        self.t_wait = Thread(target=self.wait, name="IOListener_Wait")
        self.t_wait.start()
        self.t_listen_state = Thread(target=self.listen_state, name="IOListener_Listen_State")
        self.t_listen_state.start()
        self.t_listen_loc = Thread(target=self.listen_loc, name="IOListener_Listen_Loc")
        self.t_listen_loc.start()
        while self.existing:
            while self.idle:
                time.sleep(0.02)
            self.serial_conn.initialize()
            self.send_data_to_output(self.output_start)
            while self.running:
                time.sleep(0.02)
            self.send_data_to_output(self.output_stop)

    def listen_state(self):
        while not self.running:
            time.sleep(0.02)
        while self.running:
            self.read_state_from_input()

    def listen_loc(self):
        while not self.running:
            time.sleep(0.02)
        while self.running:
            self.read_loc_from_input()

    def run(self):
        self.running = True
        self.idle = False

    def stop(self):
        self.idle = True
        self.running = False

    def extinguish(self):
        self.existing = False
        self.stop()

    def wait(self):
        while self.t_wait_running:
            controllerevent = self.proc_conn.recv()
            args = controllerevent.args
            if args == ControllerEvent.event_args_main_start:
                self.run()
            elif args == ControllerEvent.event_args_main_stop:
                self.stop()
            elif args == ControllerEvent.event_args_improc_target_found:
                self.send_data_to_output(self.output_improc)

    def send_data_to_output(self, data):
        self.serial_conn.write(data)

    def read_state_from_input(self):
        data = self.serial_conn.read_state()
        send = False
        if data == self.output_start:
            send = True
        elif data == self.input_improc:
            send = True
        elif data == self.input_finish:
            send = True
        if send:
            self.send_event(data)

    def read_loc_from_input(self):
        data = self.serial_conn.read_loc()
        self.send_event(data)

    def send_event(self, args):
        event = IOListenerEvent(args)
        self.notify_observers(event)

    def notify_observers(self, event):
        self.proc_conn.send(event)


class IOListenerEvent:
    args = None

    def __init__(self, args):
        self.args = args
