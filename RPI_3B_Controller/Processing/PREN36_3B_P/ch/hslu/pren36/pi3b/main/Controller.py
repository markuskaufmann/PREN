from threading import Thread
from multiprocessing import Process, Pipe
from ch.hslu.pren36.pi3b.comm.Communicator import communicator
from ch.hslu.pren36.pi3b.comm.CommunicatorEvent import CommunicatorEvent
from ch.hslu.pren36.pi3b.improc.ImageProcessor import ImageProcessor
from ch.hslu.pren36.pi3b.improc.ImageProcessorEvent import ImageProcessorEvent
from ch.hslu.pren36.pi3b.io.IOListener import IOListener
from ch.hslu.pren36.pi3b.main.ControllerEvent import ControllerEvent


class Controller:
    process_prefix = "PREN36_"
    proc_comm = None
    proc_improc = None
    proc_io = None
    conn_comm_parent, conn_comm_child = Pipe(duplex=True)
    conn_improc_parent, conn_improc_child = Pipe(duplex=True)
    conn_io_parent, conn_io_child = Pipe(duplex=True)
    thread_prefix = "Controller_"
    t_comm = None
    t_comm_running = True
    t_improc = None
    t_improc_running = True
    t_io = None
    t_io_running = True
    imageprocessor = ImageProcessor()
    iolistener = IOListener()

    def start(self):
        self.proc_comm = Process(target=communicator.run, name=self.process_prefix + "Communicator",
                                 args=(self.conn_comm_child,))
        self.proc_comm.start()
        self.proc_improc = Process(target=self.imageprocessor.start_idle, name=self.process_prefix + "ImageProcessing",
                                   args=(self.conn_improc_child,))
        self.proc_improc.start()
        self.proc_io = Process(target=self.iolistener.start_idle, name=self.process_prefix + "IOListener",
                               args=(self.conn_io_child,))
        self.proc_io.start()
        self.t_comm = Thread(target=self.comm_wait, name=self.thread_prefix + "Communicator")
        self.t_comm.start()
        self.t_improc = Thread(target=self.improc_wait, name=self.thread_prefix + "ImageProcessing")
        self.t_improc.start()
        self.t_io = Thread(target=self.io_wait, name=self.thread_prefix + "IOListener")
        self.t_io.start()

    def notify_observers(self, connections, event):
        for connection in connections:
            connection.send(event)

    def comm_wait(self):
        while self.t_comm_running:
            communicatorevent = self.conn_comm_parent.recv()
            controller_event_args = None
            connections = [self.conn_io_parent]
            if communicatorevent.args == CommunicatorEvent.event_args_start:
                controller_event_args = ControllerEvent.event_args_main_start
            elif communicatorevent.args == CommunicatorEvent.event_args_stop:
                controller_event_args = ControllerEvent.event_args_main_stop
                connections.append(self.conn_improc_parent)
            event = ControllerEvent(controller_event_args)
            self.notify_observers(connections, event)

    def improc_wait(self):
        while self.t_improc_running:
            imageprocessorevent = self.conn_improc_parent.recv()
            if imageprocessorevent.args == ImageProcessorEvent.event_args_found:
                event = ControllerEvent(ControllerEvent.event_args_improc_target_found)
                self.notify_observers([self.conn_comm_parent, self.conn_io_parent], event)

    def io_wait(self):
        while self.t_io_running:
            iolistenerevent = self.conn_io_parent.recv()
            data = iolistenerevent.args
            controller_event_kwargs = None
            connections = []
            if data == IOListener.output_start:
                controller_event_args = ControllerEvent.event_args_main_start
                connections.append(self.conn_comm_parent)
            elif data == IOListener.input_improc:
                controller_event_args = ControllerEvent.event_args_improc_start
                connections.append(self.conn_comm_parent)
                connections.append(self.conn_improc_parent)
            elif data == IOListener.input_finish:
                controller_event_args = ControllerEvent.event_args_main_stop
                connections.append(self.conn_improc_parent)
                connections.append(self.conn_comm_parent)
                connections.append(self.conn_io_parent)
            else:
                controller_event_args = ControllerEvent.event_args_loc_state
                controller_event_kwargs = data
                connections.append(self.conn_comm_parent)
            event = ControllerEvent(controller_event_args, controller_event_kwargs)
            self.notify_observers(connections, event)


if __name__ == '__main__':
    controller = Controller()
    controller.start()
