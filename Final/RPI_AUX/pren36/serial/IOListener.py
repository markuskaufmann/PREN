import time
from threading import Thread

from pren36.serial.IOListenerEvent import IOListenerEvent
from pren36.serial.SerialConnection import SerialConnection
from pren36.controller.ControllerEvent import ControllerEvent


class IOListener:
    output_start = "start"
    output_stop = "stop"
    output_improc = "improc_found"
    input_improc = "improc_launch"
    input_loc = "loc"
    input_finish = "finish"

    proc_conn = None
    serial_conn = None
    t_wait = None
    t_wait_running = True
    t_read = None
    t_read_running = True

    def start_idle(self, conn):
        self.proc_conn = conn
        self.serial_conn = SerialConnection()
        self.t_wait = Thread(target=self.wait, name="IOListener_Wait")
        self.t_wait.start()
        self.t_read = Thread(target=self.read, name="IOListener_Read")
        self.t_read.start()
        self.serial_conn.initialize()

    def wait(self):
        while self.t_wait_running:
            controllerevent = self.proc_conn.recv()
            args = controllerevent.args
            if args == ControllerEvent.event_args_main_start:
                self.send_data_to_output(self.output_start)
            elif args == ControllerEvent.event_args_main_stop:
                self.send_data_to_output(self.output_stop)
            elif args == ControllerEvent.event_args_improc_target_found:
                self.send_data_to_output(self.output_improc)

    def send_data_to_output(self, data):
        self.serial_conn.write(data)

    def read(self):
        while self.t_read_running:
            data = self.serial_conn.read()
            self.send_event(data)
            time.sleep(0.05)

    def send_event(self, args):
        event = IOListenerEvent(args)
        self.notify_observers(event)

    def notify_observers(self, event):
        self.proc_conn.send(event)
