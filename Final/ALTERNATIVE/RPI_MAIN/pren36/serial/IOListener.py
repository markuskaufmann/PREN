import time
from queue import Queue
from threading import Thread, Lock

from pren36.serial.SerialConnection import SerialConnection


class IOListener:

    serial_conn = None
    t_write = None
    t_write_running = True
    t_read = None
    t_read_running = True
    lock = Lock()

    def __init__(self, fsm_queue):
        self.fsm_queue = fsm_queue
        self.loc_queue = Queue()

    def start_idle(self):
        self.serial_conn = SerialConnection()
        self.serial_conn.initialize()
        self.t_read = Thread(target=self.read, name="IOListener_Read")
        self.t_read.start()

    def send_data_to_output(self, event):
        with self.lock:
            self.serial_conn.write(event.args)

    def read(self):
        while self.t_read_running:
            data = self.serial_conn.read()
            if len(data) == 0:
                continue
            self.send_event(data)
            time.sleep(0.05)

    def send_event(self, args):
        self.fsm_queue.put(args)
