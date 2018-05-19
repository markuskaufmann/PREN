import time
from threading import Thread

from pren36.controller.ControllerEvent import ControllerEvent
from pren36.serial.SerialConnection import SerialConnection


class IOListener:
    output_start = "start"
    output_stop = "stop"
    output_improc = "improc_found"
    input_improc = "improc_launch"
    input_loc = "loc"
    input_finish = "finish"

    serial_conn = None
    t_read = None
    t_read_running = True

    def __init__(self, controller_queue):
        self.controller_queue = controller_queue

    def start_idle(self):
        self.serial_conn = SerialConnection()
        self.t_read = Thread(target=self.read, name="IOListener_Read")
        self.t_read.start()
        self.serial_conn.initialize()

    def send_data_to_output(self, event):
        data = event.args
        if data == ControllerEvent.event_args_main_start:
            data = self.output_start
        elif data == ControllerEvent.event_args_main_stop:
            data = self.output_stop
        elif data == ControllerEvent.event_args_improc_target_found:
            data = self.output_improc
        self.serial_conn.write(data)

    def read(self):
        while self.t_read_running:
            data = self.serial_conn.read()
            self.send_event(data)
            time.sleep(0.05)

    def send_event(self, args):
        self.controller_queue.put(args)
