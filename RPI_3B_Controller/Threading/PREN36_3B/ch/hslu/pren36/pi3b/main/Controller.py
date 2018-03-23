from threading import Thread
from ch.hslu.pren36.pi3b.comm.Communicator import communicator
from ch.hslu.pren36.pi3b.improc.ImageProcessor import ImageProcessor
from ch.hslu.pren36.pi3b.io.IOListener import IOListener


class Controller:
    thread_prefix = "Controller_"
    comm_thread = None
    improc_thread = None
    iolistener_thread = None
    callbacks = set()
    imageprocessor = ImageProcessor()
    iolistener = IOListener()

    def start(self):
        self.comm_thread = Thread(target=communicator.run, name=self.thread_prefix + "Communicator")
        self.comm_thread.start()
        self.add_callback(communicator.on_state_changed)
        communicator.add_callback(self.on_comm_triggered)
        self.improc_thread = Thread(target=self.imageprocessor.start_idle, name=self.thread_prefix + "ImageProcessing")
        self.improc_thread.start()
        self.imageprocessor.add_callback(self.on_target_found)
        self.iolistener_thread = Thread(target=self.iolistener.start_idle, name=self.thread_prefix + "IOListener")
        self.iolistener_thread.start()
        self.iolistener.add_callback(self.on_io_event)

    def run_image_processing(self):
        self.imageprocessor.run()

    def stop_image_processing(self):
        self.imageprocessor.stop()

    def start_io_listening(self):
        self.iolistener.run()

    def stop_io_listening(self):
        self.iolistener.stop()

    def on_comm_triggered(self, communicatorevent):
        if communicatorevent.args == communicator.event_args_start:
            self.run_image_processing()
            self.start_io_listening()
        elif communicatorevent.args == communicator.event_args_stop:
            self.stop_image_processing()
            self.stop_io_listening()

    def on_target_found(self, imageprocessorevent):
        if imageprocessorevent.args == 1:
            event = ControllerEvent("Target found")
            self.notify_observers(event)

    def on_io_event(self, iolistenerevent):
        data = iolistenerevent.args
        if data == self.iolistener.input_improc:
            # self.io_start_improc()
            print("start improc")
        elif data == self.iolistener.input_finish:
            # self.io_finish()
            print("stop proc")
        else:
            loc = data.split(";")
            # self.io_loc(loc)
            print("location")

    def add_callback(self, callback):
        self.callbacks.add(callback)

    def notify_observers(self, event):
        for callback in self.callbacks:
            callback(event)


class ControllerEvent:
    args = None

    def __init__(self, args):
        self.args = args


if __name__ == '__main__':
    controller = Controller()
    controller.start()
