import time
from threading import Thread

from pren36.serial.SerialConnection import SerialConnection


class IOListener:

    serial_conn = None
    t_read = None
    t_read_running = True

    def __init__(self, controller_queue):
        self.controller_queue = controller_queue

    def start_idle(self):
        self.serial_conn = SerialConnection()
        self.serial_conn.initialize()
        self.t_read = Thread(target=self.read, name="IOListener_Read")
        self.t_read.start()

    def send_data_to_output(self, event):
        self.serial_conn.write(event.args)

    def read(self):
        while self.t_read_running:
            data = self.serial_conn.read()
            if len(data) == 0:
                continue
            self.send_event(data)
            time.sleep(0.05)

    def send_event(self, args):
        self.controller_queue.put(args)
