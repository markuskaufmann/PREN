from queue import Queue
from threading import Thread
from ch.hslu.pren36.pi3b.io.SimFSM import SimFSM


class SimSerialConnection:
    fsm = SimFSM()
    t_fsm = None
    fsm_state_queue = Queue()
    fsm_loc_queue = Queue()

    def initialize(self):
        self.t_fsm = Thread(target=self.fsm.start_idle, name="SimFSM_Processor")
        self.t_fsm.start()
        self.fsm.set_queues(self.fsm_state_queue, self.fsm_loc_queue)
        self.fsm.run()

    def write(self, data):
        self.fsm.transmit(data)

    def read_state(self):
        return self.fsm_state_queue.get()

    def read_loc(self):
        return self.fsm_loc_queue.get()
