import time
from threading import Thread
from ch.hslu.pren36.pi3b.ultrasound.UltrasoundSensor import UltraSoundSensor


class ControllerUltraSoundSensor:
    idle = True
    running = False
    t_running = None
    uss = None

    def __init__(self):
        self.uss = UltraSoundSensor()
        self.t_running = Thread(target=self.start_idle)
        self.t_running.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        try:
            while self.running:
                print("distance(x) = %.2f cm" % self.uss.distance())
                time.sleep(0.5)
        except KeyboardInterrupt:
            self.uss.stop()
            return

    def run(self):
        self.running = True
        self.idle = False


if __name__ == '__main__':
    cuss = ControllerUltraSoundSensor()
    cuss.run()
