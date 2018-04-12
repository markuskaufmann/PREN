import time
from threading import Thread
from ch.hslu.pren36.pi3b.stepmotorFahrwerk.StepmotorFahrwerk import StepmotorFahrwerk


class ControllerStepmotorFahrwerk:
    idle = True
    running = False
    t_running = None
    t_sm = None
    sm = None

    def __init__(self):
        self.sm = StepmotorFahrwerk()
        self.t_running = Thread(target=self.start_idle)
        self.t_running.start()
        self.t_sm = Thread(target=self.sm.control)
        self.t_sm.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        while self.running:
            time.sleep(1)
            self.sm.set_state(StepmotorFahrwerk.state['acc'])
            time.sleep(10)
            self.sm.set_state(StepmotorFahrwerk.state['stop'])
            self.running = False

    def run(self):
        self.running = True
        self.idle = False


if __name__ == '__main__':
    csm = ControllerStepmotorFahrwerk()
    csm.run()
