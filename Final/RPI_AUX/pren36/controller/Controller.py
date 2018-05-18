import time
from queue import Queue
from threading import Thread
from multiprocessing import Process, Pipe
from pren36.communicator.Communicator import communicator
from pren36.communicator.CommunicatorEvent import CommunicatorEvent
from pren36.improc.ImageProcessorPiCamera import ImageProcessorPiCamera
from pren36.improc.ImageProcessorEvent import ImageProcessorEvent
from pren36.sensor.TOFSensor import TOFSensor
from pren36.sensor.UltrasoundSensor import UltraSoundSensor
from pren36.serial.IOListener import IOListener
from pren36.controller.ControllerEvent import ControllerEvent


class Controller:
    process_prefix = "PREN36_"
    proc_comm = None
    proc_improc = None
    conn_comm_parent, conn_comm_child = Pipe(duplex=True)
    conn_improc_parent, conn_improc_child = Pipe(duplex=True)
    thread_prefix = "Controller_"
    t_comm = None
    t_comm_running = True
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
        self.proc_comm = Process(target=communicator.run, name=self.process_prefix + "Communicator",
                                 args=(self.conn_comm_child,))
        self.proc_comm.start()
        self.proc_improc = Process(target=self.imageprocessor.start_idle, name=self.process_prefix + "ImageProcessing",
                                   args=(self.conn_improc_child,))
        self.proc_improc.start()
        self.t_comm = Thread(target=self.comm_wait, name=self.thread_prefix + "Communicator")
        self.t_comm.start()
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

    def comm_wait(self):
        while self.t_comm_running:
            communicatorevent = self.conn_comm_parent.recv()
            controller_event_args = None
            if communicatorevent.args == CommunicatorEvent.event_args_start:
                controller_event_args = ControllerEvent.event_args_main_start
            elif communicatorevent.args == CommunicatorEvent.event_args_stop:
                controller_event_args = ControllerEvent.event_args_main_stop
            event = ControllerEvent(controller_event_args)
            self.io_send(event)

    def improc_wait(self):
        while self.t_improc_running:
            imageprocessorevent = self.conn_improc_parent.recv()
            if imageprocessorevent.args == ImageProcessorEvent.event_args_found:
                event = ControllerEvent(ControllerEvent.event_args_improc_target_found)
                self.notify_observers([self.conn_comm_parent], event)
                self.io_send(event)

    def io_send(self, event):
        self.iolistener.send_data_to_output(event)

    def io_wait(self):
        while self.t_io_running:
            data = self.rec_queue.get()
            controller_event_args = None
            controller_event_kwargs = None
            connections = []
            if data == IOListener.output_start:
                controller_event_args = ControllerEvent.event_args_main_start
                connections.append(self.conn_comm_parent)
            elif data == IOListener.output_stop:
                controller_event_args = ControllerEvent.event_args_main_stop
                connections.append(self.conn_comm_parent)
            elif data == IOListener.input_improc:
                controller_event_args = ControllerEvent.event_args_improc_start
                connections.append(self.conn_comm_parent)
                connections.append(self.conn_improc_parent)
            elif data == IOListener.input_finish:
                controller_event_args = ControllerEvent.event_args_main_stop
                connections.append(self.conn_improc_parent)
                connections.append(self.conn_comm_parent)
            else:
                controller_event_args = ControllerEvent.event_args_loc_state
                controller_event_kwargs = data
                connections.append(self.conn_comm_parent)
            event = ControllerEvent(controller_event_args, controller_event_kwargs)
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
