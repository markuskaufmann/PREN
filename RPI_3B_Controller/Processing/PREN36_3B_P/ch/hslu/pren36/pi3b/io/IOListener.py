import time
from threading import Thread
from ch.hslu.pren36.pi3b.io.SerialConnection import SerialConnection
from ch.hslu.pren36.pi3b.main.ControllerEvent import ControllerEvent


class IOListener:
    proc_conn = None
    t_wait = None
    serial_conn = SerialConnection()
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
        while self.existing:
            while self.idle:
                time.sleep(0.02)
            self.serial_conn.initialize()
            self.send_data_to_output(self.output_start)
            self.listen()
            self.send_data_to_output(self.output_stop)

    def listen(self):
        while self.running:
            self.read_data_from_input()

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
        controllerevent = self.proc_conn.recv()
        args = controllerevent.args
        print(args)
        if args == ControllerEvent.event_args_main_start:
            self.run()
        elif args == ControllerEvent.event_args_main_stop:
            self.stop()
        elif args == ControllerEvent.event_args_improc_target_found:
            self.send_data_to_output(self.output_improc)

    def send_data_to_output(self, data):
        self.serial_conn.write(data)

    def read_data_from_input(self):
        data = self.serial_conn.read()
        send = False
        if data == self.input_improc:
            send = True
        elif data == self.input_finish:
            send = True
        elif data.split(";")[0] == self.input_loc:
            send = True
        if send:
            self.send_event(data)
        print(data)

    def send_event(self, args):
        event = IOListenerEvent(args)
        self.notify_observers(event)

    def notify_observers(self, event):
        self.proc_conn.send(event)


class IOListenerEvent:
    args = None

    def __init__(self, args):
        self.args = args
