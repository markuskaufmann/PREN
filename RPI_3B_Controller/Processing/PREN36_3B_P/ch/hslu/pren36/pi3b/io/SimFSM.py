import time
from ch.hslu.pren36.pi3b.io.SysPseudo import SysPseudo


class SimFSM:
    existing = True
    idle = True
    signal_start = "start"
    signal_stop = "stop"
    signal_finish = "finish"
    signal_object = "improc_launch"
    signal_loc = "loc"
    signal_improc_found = "improc_found"
    start_set = False
    stop_set = False
    improc_set = False
    sys_pseudo = SysPseudo()
    state_queue = None
    loc_queue = None

    def start_idle(self):
        while self.existing:
            while self.idle:
                time.sleep(0.02)
            self.simulate()

    def set_queues(self, state_queue, loc_queue):
        self.state_queue = state_queue
        self.loc_queue = loc_queue

    def run(self):
        self.idle = False

    def stop(self):
        self.idle = True

    def transmit(self, data):
        if data == self.signal_start:
            self.start_set = True
        elif data == self.signal_stop:
            self.stop_set = True
        elif data == self.signal_improc_found:
            self.improc_set = True

    def simulate(self):
        while not self.start_set:
            time.sleep(0.02)
        self.state_queue.put(self.signal_start)
        self.sys_pseudo.start(self.loc_queue)
        time.sleep(5)
        self.state_queue.put(self.signal_object)
        while not self.improc_set:
            time.sleep(0.02)
        time.sleep(5)
        self.state_queue.put(self.signal_finish)
        self.stop()
