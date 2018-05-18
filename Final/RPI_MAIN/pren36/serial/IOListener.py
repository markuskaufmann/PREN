import time
from queue import Queue
from threading import Thread

from pren36.fsm.ControllerEvent import ControllerEvent
from pren36.serial.IOListenerEvent import IOListenerEvent
from pren36.serial.SerialConnection import SerialConnection


class IOListener:
    output_start = "start"
    output_stop = "stop"
    output_improc = "improc_found"
    input_improc = "improc_launch"
    input_loc = "loc"
    input_finish = "finish"

    serial_conn = None
    t_write = None
    t_write_running = True
    t_read = None
    t_read_running = True

    def __init__(self, fsm_queue):
        self.fsm_queue = fsm_queue
        self.loc_queue = Queue()

    def start_idle(self, conn):
        self.serial_conn = SerialConnection()
        self.t_write = Thread(target=self.write, name="IOListener_Write")
        self.t_write.start()
        self.t_read = Thread(target=self.read, name="IOListener_Read")
        self.t_read.start()
        self.serial_conn.initialize()

    def send_data_to_output(self, event):
        data = event.args
        if data == ControllerEvent.event_args_main_start:
            data = self.output_start
        elif data == ControllerEvent.event_args_main_stop:
            data = self.output_stop
        elif data == ControllerEvent.event_args_main_finish:
            data = self.input_finish
        elif data == ControllerEvent.event_args_improc_start:
            data = self.input_improc
        self.serial_conn.write(data)

    def send_loc_to_output(self, loc):
        self.loc_queue.put(loc)

    def write(self):
        while self.t_write_running:
            data = self.loc_queue.get()
            self.serial_conn.write(data)

    def read(self):
        while self.t_read_running:
            data = self.serial_conn.read()
            self.send_event(data)
            time.sleep(0.05)

    def send_event(self, args):
        self.fsm_queue.put(args)
