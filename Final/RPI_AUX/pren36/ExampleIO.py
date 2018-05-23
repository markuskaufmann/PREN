import time
from queue import Queue
from threading import Thread

from pren36.controller.ControllerEvent import ControllerEvent
from pren36.serial.IOListener import IOListener


class Launcher:
    queue = Queue()
    iolistener = None
    writing = True
    reading = True

    def __init__(self):
        self.idle = True
        self.iolistener = IOListener(self.queue)
        self.iolistener.start_idle()
        time.sleep(2)
        t_write = Thread(target=self.write)
        t_write.start()
        t_read = Thread(target=self.read)
        t_read.start()

    def write(self):
        while self.writing:
            event = ControllerEvent(ControllerEvent.event_args_main_stop)
            self.iolistener.send_data_to_output(event)
            time.sleep(0.5)

    def read(self):
        while self.reading:
            data = self.queue.get()
            print(data)


if __name__ == '__main__':
    Launcher()
