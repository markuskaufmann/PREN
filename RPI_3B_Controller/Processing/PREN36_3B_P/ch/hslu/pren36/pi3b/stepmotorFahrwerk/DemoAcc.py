import time
from threading import Thread


class DemoAcc:
    idle = True
    t_main = None

    steps_acc = 0
    delay = 1 / 100  # 0.0208 / 2
    delay_drive = 1 / 600  # 0.0005 / 4096

    SPR = 48

    def __init__(self):
        self.t_main = Thread(target=self.start_idle)
        self.t_main.start()

    def start_idle(self):
        while self.idle:
            time.sleep(0.02)
        print("res: " + str(self.accelerate(self.delay)))
        print("steps: " + str(self.steps_acc))
        print("revs: " + str(self.steps_acc / DemoAcc.SPR))

    def accelerate(self, delay):
        while delay > self.delay_drive:
            # GPIO.output(StepmotorFahrwerk.STEP, GPIO.HIGH)
            time.sleep(delay)
            # GPIO.output(StepmotorFahrwerk.STEP, GPIO.LOW)
            time.sleep(delay)
            delay /= 1.01
            self.steps_acc += 1
            print(delay)
        return delay

    def run(self):
        self.idle = False


if __name__ == '__main__':
    da = DemoAcc()
    da.run()
