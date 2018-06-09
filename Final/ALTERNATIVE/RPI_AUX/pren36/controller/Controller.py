import time
from queue import Queue
from threading import Thread
from multiprocessing import Process, Pipe
from pren36.improc.ImageProcessorPiCamera import ImageProcessorPiCamera
from pren36.improc.ImageProcessorEvent import ImageProcessorEvent
from pren36.sensor.TOFSensor import TOFSensor
from pren36.sensor.UltrasoundSensor import UltraSoundSensor
from pren36.serial.IOListener import IOListener
from pren36.controller.ControllerEvent import ControllerEvent


class Controller:
    process_prefix = "PREN36_"
    proc_improc = None
    conn_improc_parent, conn_improc_child = Pipe(duplex=True)
    thread_prefix = "Controller_"
    t_improc = None
    t_improc_running = True
    t_io = None
    t_io_running = True
    t_us = None
    t_us_running = True
    t_us_control = False
    t_tof = None
    t_tof_running = True
    t_tof_control = False
    imageprocessor = ImageProcessorPiCamera()
    rec_queue = Queue()
    iolistener = IOListener(rec_queue)
    ultrasonic = UltraSoundSensor()
    tof = TOFSensor()

    def start(self):
        self.iolistener.start_idle()
        self.proc_improc = Process(target=self.imageprocessor.start_idle, name=self.process_prefix + "ImageProcessing",
                                   args=(self.conn_improc_child,))
        self.proc_improc.start()
        self.t_improc = Thread(target=self.improc_wait, name=self.thread_prefix + "ImageProcessing")
        self.t_improc.start()
        self.t_io = Thread(target=self.io_wait, name=self.thread_prefix + "IOListener")
        self.t_io.start()
        self.t_us = Thread(target=self.control_ultrasonic, name=self.thread_prefix + "LocX")
        self.t_us.start()
        self.t_tof = Thread(target=self.control_tof, name=self.thread_prefix + "LocZ")
        self.t_tof.start()

    def notify_observers(self, connections, event):
        for connection in connections:
            connection.send(event)

    def improc_wait(self):
        while self.t_improc_running:
            imageprocessorevent = self.conn_improc_parent.recv()
            if imageprocessorevent.args == ImageProcessorEvent.event_args_found:
                event = ControllerEvent(ControllerEvent.event_args_improc_target_found)
                self.io_send(event)

    def io_send(self, event):
        self.iolistener.send_data_to_output(event)

    def io_wait(self):
        while self.t_io_running:
            data = self.rec_queue.get()
            connections = []
            data = str(data).strip()
            if len(data) == 0:
                continue
            if data == str(ControllerEvent.event_args_improc_start) or data == str(ControllerEvent.event_args_main_stop):
                event = ControllerEvent(data)
                connections.append(self.conn_improc_parent)
                self.notify_observers(connections, event)

    def control_ultrasonic(self):
        while self.t_us_running:
            while not self.t_us_control:
                time.sleep(0.02)
            while self.t_us_control:
                print(self.ultrasonic.distance())
                time.sleep(1)

    def control_tof(self):
        while self.t_tof_running:
            while not self.t_tof_control:
                time.sleep(0.02)
            while self.t_tof_control:
                print(self.tof.distance())
                time.sleep(1)
