import time
from threading import Thread
from ch.hslu.pren36.pi3b.ultrasound.UltrasoundSensor import UltraSoundSensor


class ControllerTOFSensor:
    idle = True
    running = False
    t_running = None
    ts = None

    def __init__(self):
        self.ts = UltraSoundSensor()
        self.t_running = Thread(target=self.start_idle)
        self.t_running.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        try:
            while self.running:
                print("distance(x) = %.2f cm" % self.ts.distance())
                time.sleep(0.5)
        except KeyboardInterrupt:
            self.ts.stop()
            return

    def run(self):
        self.running = True
        self.idle = False


if __name__ == '__main__':
    cts = ControllerTOFSensor()
    cts.run()
