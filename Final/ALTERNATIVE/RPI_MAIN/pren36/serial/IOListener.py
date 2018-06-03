import time
from queue import Queue
from threading import Thread

from pren36.serial.SerialConnection import SerialConnection


class IOListener:

    serial_conn = None
    t_write = None
    t_write_running = True
    t_read = None
    t_read_running = True

    def __init__(self, fsm_queue):
        self.fsm_queue = fsm_queue
        self.loc_queue = Queue()

    def start_idle(self):
        self.serial_conn = SerialConnection()
        self.serial_conn.initialize()
        self.t_write = Thread(target=self.write, name="IOListener_Write")
        self.t_write.start()
        self.t_read = Thread(target=self.read, name="IOListener_Read")
        self.t_read.start()

    def send_data_to_output(self, event):
        self.serial_conn.write(event.args)

    def send_loc_to_output(self, loc):
        self.loc_queue.put(loc)

    def write(self):
        while self.t_write_running:
            data = self.loc_queue.get()
            self.serial_conn.write(data)

    def read(self):
        while self.t_read_running:
            data = self.serial_conn.read()
            if len(data) == 0:
                continue
            self.send_event(data)
            time.sleep(0.05)

    def send_event(self, args):
        self.fsm_queue.put(args)
