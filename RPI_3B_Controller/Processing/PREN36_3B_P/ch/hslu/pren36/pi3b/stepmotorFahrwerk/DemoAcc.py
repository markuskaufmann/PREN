import math
import time
import numpy as np


class DemoAcc:
    RPM = 100
    RPS = RPM / 60
    SPR = 200
    STEP_MOD = 2  # 1/2 Step
    SPS = RPS * (SPR * STEP_MOD)
    DIA_MOTOR = 5  # [mm]
    DIA = 85  # [mm]
    DIA_MOD = DIA / DIA_MOTOR
    PER = DIA_MOTOR * np.pi  # [mm]
    DPS = PER / SPR

    steps = 0
    steps_acc = 0
    steps_stop = 0
    def_steps_acc = 0
    def_steps_stop = 0
    delay_drive = 1 / (SPS * 2)  # 0.0005 / 4096
    delay = delay_drive * 8  # 0.0208 / 2

    def __init__(self):
        pass

    def accelerate(self, delay, steps):
        print("on accelerate")
        while delay > self.delay_drive and steps != 0:
            # GPIO.output(StepmotorFahrwerk.STEP, GPIO.HIGH)
            time.sleep(delay)
            # GPIO.output(StepmotorFahrwerk.STEP, GPIO.LOW)
            time.sleep(delay)
            delay /= 1.01
            steps -= 1
        return delay

    def drive(self, delay, step_count):
        print("on drive")
        for step in range(0, step_count):
            # GPIO.output(StepmotorFahrwerk.STEP, GPIO.HIGH)
            time.sleep(delay)
            # GPIO.output(StepmotorFahrwerk.STEP, GPIO.LOW)
            time.sleep(delay)

    def stop(self, delay, steps):
        print("on stop")
        while delay < self.delay and steps != 0:
            # GPIO.output(StepmotorFahrwerk.STEP, GPIO.HIGH)
            time.sleep(delay)
            # GPIO.output(StepmotorFahrwerk.STEP, GPIO.LOW)
            time.sleep(delay)
            delay *= 1.01
            steps -= 1
        return delay

    def calc_acc(self, delay, steps):
        self.steps_acc = 0
        while delay > self.delay_drive and steps != 0:
            delay /= 1.01
            steps -= 1
            self.steps_acc += 1
        return delay, steps

    def calc_stop(self, delay, steps):
        self.steps_stop = 0
        while delay < self.delay and steps != 0:
            delay *= 1.01
            steps -= 1
            self.steps_stop += 1
        return steps

    def move_distance(self, distance_mm):
        self.control(distance_mm)

    def control(self, distance_mm):
        distance = distance_mm
        print("distance: %d mm" % distance)
        revs = (distance / DemoAcc.PER) / DemoAcc.DIA_MOD
        print(revs)
        self.steps = int(math.ceil(revs * DemoAcc.SPR * DemoAcc.STEP_MOD))
        print("steps: %d" % self.steps)
        d_acc, s_acc = self.calc_acc(self.delay, self.steps)
        s_stop = self.calc_stop(d_acc, self.steps)
        steps_acc_stop = self.steps_acc
        print("acc steps theoretical: %d" % self.steps_acc)
        print("stop steps theoretical: %d" % self.steps_stop)
        if self.steps < (self.steps_acc + self.steps_stop):
            steps_acc_stop = int(math.ceil(self.steps / 2))
        print("acc / stop steps: %d" % steps_acc_stop)
        s_drive = self.steps - steps_acc_stop * 2
        print("drive steps: %d" % s_drive)

        delay = self.delay
        now = time.time()
        delay = self.accelerate(delay, steps_acc_stop)
        self.drive(delay, s_drive)
        self.stop(delay, steps_acc_stop)
        duration = time.time() - now
        print("steps total: %d" % (steps_acc_stop * 2 + s_drive))
        print("duration: " + str(duration))


if __name__ == '__main__':
    da = DemoAcc()
    da.move_distance(200)
