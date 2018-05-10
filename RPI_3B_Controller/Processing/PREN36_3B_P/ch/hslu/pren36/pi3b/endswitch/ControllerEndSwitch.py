import time
from threading import Thread
from ch.hslu.pren36.pi3b.endswitch.EndSwitch import EndSwitch


class ControllerEndSwitch:
    idle = True
    running = False
    t_running = None
    es = None

    def __init__(self):
        self.es = EndSwitch()
        self.t_running = Thread(target=self.start_idle)
        self.t_running.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        try:
            while self.running:
                print("signal = %d" % self.es.signal())
                time.sleep(0.2)
        except KeyboardInterrupt:
            self.es.stop()
            return

    def run(self):
        self.running = True
        self.idle = False


if __name__ == '__main__':
    ces = ControllerEndSwitch()
    ces.run()
