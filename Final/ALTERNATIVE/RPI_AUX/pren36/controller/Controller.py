import time
from multiprocessing import Process, Pipe
from queue import Queue
from threading import Thread

from pren36.communicator.CommObject import CommObject
from pren36.communicator.Communicator import communicator
from pren36.controller.ControllerEvent import ControllerEvent
from pren36.improc.ImageProcessorEvent import ImageProcessorEvent
from pren36.improc.ImageProcessorPiCamera import ImageProcessorPiCamera
from pren36.sensor.TOFSensor import TOFSensor
from pren36.serial.IOListener import IOListener


class Controller:
    process_prefix = "PREN36_"
    proc_comm = None
    comm_object = None
    proc_improc = None
    conn_improc_parent, conn_improc_child = Pipe(duplex=True)
    thread_prefix = "Controller_"
    t_improc = None
    t_comm_start = None
    start_sent = False
    stop_sent = False
    t_comm_stop = None
    t_io = None
    t_tof = None
    # t_tof_send = False
    imageprocessor = ImageProcessorPiCamera()
    rec_queue = Queue()
    iolistener = IOListener(rec_queue)
    tof = TOFSensor()

    def start(self):
        self.iolistener.start_idle()
        self.comm_object = CommObject()
        self.comm_object.reset()
        self.proc_comm = Process(target=communicator.run, name=self.process_prefix + "Communicator",
                                 args=(self.comm_object,))
        self.proc_comm.start()
        self.proc_improc = Process(target=self.imageprocessor.start_idle, name=self.process_prefix + "ImageProcessing",
                                   args=(self.conn_improc_child,))
        self.proc_improc.start()
        self.t_improc = Thread(target=self.improc_wait, name=self.thread_prefix + "ImageProcessing")
        self.t_improc.start()
        self.t_io = Thread(target=self.io_wait, name=self.thread_prefix + "IOListener")
        self.t_io.start()
        self.t_comm_start = Thread(target=self.comm_wait_start, name=self.thread_prefix + "CommStart")
        self.t_comm_start.start()
        self.t_comm_stop = Thread(target=self.comm_wait_stop, name=self.thread_prefix + "CommStop")
        self.t_comm_stop.start()
        # self.t_tof = Thread(target=self.control_tof, name=self.thread_prefix + "TOF")
        # self.t_tof.start()

    def improc_wait(self):
        while True:
            imageprocessorevent = self.conn_improc_parent.recv()
            if imageprocessorevent.args == ImageProcessorEvent.event_args_found:
                event = ControllerEvent(ControllerEvent.event_args_improc_target_found)
                self.iolistener.send_data_to_output(event)

    def io_wait(self):
        while True:
            data = self.rec_queue.get()
            data = str(data).strip()
            if len(data) == 0:
                continue
            if data == str(ControllerEvent.event_args_improc_start):
                event = ControllerEvent(data)
                self.conn_improc_parent.send(event)
            elif data == str(ControllerEvent.event_args_req_height):
                self.iolistener.send_str_to_output(self.get_z())
            elif data == str(ControllerEvent.event_args_main_finish):
                self.reset()
            else:
                parts = data.split(";")
                self.comm_object.update_state(parts[0])
                self.comm_object.update_x(parts[1])
                z = self.get_z()
                self.comm_object.update_z(z - (z - float(parts[2])))

    def comm_wait_start(self):
        while True:
            while not self.comm_object.is_started():
                time.sleep(0.5)
            if not self.start_sent:
                # self.comm_object.reset()
                event = ControllerEvent(ControllerEvent.event_args_main_start)
                self.iolistener.send_data_to_output(event)
                self.start_sent = True
                # time.sleep(0.5)
                # self.t_tof_send = True
            time.sleep(1)

    def comm_wait_stop(self):
        while True:
            while not self.comm_object.is_stopped():
                time.sleep(0.5)
            if not self.stop_sent:
                event = ControllerEvent(ControllerEvent.event_args_main_stop)
                self.iolistener.send_data_to_output(event)
                self.stop_sent = True
                # self.t_tof_send = False
            time.sleep(1)

    # def control_tof(self):
    #     while True:
    #         if self.t_tof_send:
    #             distance = self.tof.distance() - 19.5
    #             self.iolistener.send_data_to_output(ControllerEvent(distance))
    #         time.sleep(0.5)

    def get_z(self):
        return float(self.tof.distance()) - 19.5

    def reset(self):
        # self.comm_object.reset()
        self.start_sent = False
        self.stop_sent = False
        # self.t_tof_send = False
