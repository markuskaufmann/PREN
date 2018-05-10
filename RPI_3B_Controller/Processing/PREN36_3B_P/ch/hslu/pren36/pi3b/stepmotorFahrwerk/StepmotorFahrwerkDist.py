import math
from time import sleep
import RPi.GPIO as GPIO
import numpy as np
from ch.hslu.pren36.pi3b.stepmotorFahrwerk.AccMode import AccMode


class StepmotorFahrwerk:
    DIR = 26  # Direction GPIO Pin GREEN
    STEP = 13  # Step GPIO Pin BLUE
    CW = 1  # Clockwise Rotation
    CCW = 0  # Counterclockwise Rotation
    RPM = 200
    RPS = RPM / 60
    SPR = 400
    STEP_MOD = 2  # 1/2 Step
    SPS = RPS * (SPR * STEP_MOD)
    DIA = 85  # [mm]
    PER = DIA * np.pi  # [mm]

    STATES = {
        'stop': 0,
        'acc': 1,
        'drive': 2
    }
    STATE_ACC = STATES['acc']
    STATE_DRIVE = STATES['drive']
    STATE_STOP = STATES['stop']

    # Einstellungen Mode 0|1|2
    # Müssen auf Hardware geändert werden!
    # 000 Fullstep
    # 100 1/2 Step
    # 010 1/4 Step
    # 110 8 microstep/step
    # 001 16 microstep/step
    # 101 32 microstep/step

    distance = 0
    steps = 0
    steps_acc = 0
    steps_drive = 0
    steps_stop = 0
    steps_acc_stop = 0
    delay_drive = 1 / (SPS * 2)  # 0.0005 / 4096
    delay = delay_drive * 3  # 0.0208 / 2
    current_state = STATE_STOP
    current_direction = CW
    current_acc = AccMode.MODE_START[2]
    accelerating = False

    def __init__(self, direction):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(StepmotorFahrwerk.DIR, GPIO.OUT)
        GPIO.setup(StepmotorFahrwerk.STEP, GPIO.OUT)
        self.set_direction(direction)

    def set_state(self, state):
        self.current_state = state

    def set_acc_mode(self, mode):
        self.current_acc = mode

    def set_direction(self, direction):
        self.current_direction = direction
        self.set_state(StepmotorFahrwerk.STATE_STOP)
        GPIO.output(StepmotorFahrwerk.DIR, self.current_direction)

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

    def calc_steps(self, distance_cm):
        if distance_cm == -1:
            self.distance = -1
            self.steps = -1
        else:
            self.distance = distance_cm * 10
            revs = self.distance / StepmotorFahrwerk.PER
            self.steps = int(math.ceil(revs * StepmotorFahrwerk.SPR))
        d_acc, s_acc = self.calc_acc(self.delay, self.steps)
        s_stop = self.calc_stop(d_acc, self.steps)
        self.steps_acc_stop = self.steps_acc
        if self.steps != -1 and self.steps < (self.steps_acc + self.steps_stop):
            self.steps_acc_stop = int(math.ceil(self.steps / 2))
        if self.steps == -1:
            self.steps_drive = -1
        else:
            self.steps_drive = self.steps - self.steps_acc_stop * 2

    def accelerate(self, delay, steps):
        while delay > self.delay_drive and steps != 0:
            GPIO.output(StepmotorFahrwerk.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(StepmotorFahrwerk.STEP, GPIO.LOW)
            sleep(delay)
            delay /= 1.01
            steps -= 1
        return delay

    def stop(self, delay, steps):
        while delay < self.delay and steps != 0:
            GPIO.output(StepmotorFahrwerk.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(StepmotorFahrwerk.STEP, GPIO.LOW)
            sleep(delay)
            delay *= 1.01
            steps -= 1
        return delay

    def drive(self, delay, step_count):
        steps = 0
        while steps < step_count or step_count == -1:
            GPIO.output(StepmotorFahrwerk.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(StepmotorFahrwerk.STEP, GPIO.LOW)
            sleep(delay)
            steps += 1

    def move_distance(self, distance_cm, acc_mode):
        self.calc_steps(distance_cm)
        self.set_acc_mode(acc_mode[2])
        self.set_state(StepmotorFahrwerk.STATE_ACC)

    def move_continuous(self, acc_mode):
        self.calc_steps(-1)
        self.set_acc_mode(acc_mode[2])
        self.set_state(StepmotorFahrwerk.STATE_ACC)

    def control(self):
        delay = StepmotorFahrwerk.delay
        while True:
            if self.current_state == StepmotorFahrwerk.STATE_DRIVE:
                while self.current_state is not StepmotorFahrwerk.STATE_STOP:
                    self.drive(delay, self.steps_drive)
                    self.set_state(StepmotorFahrwerk.STATE_STOP)
            elif self.current_state == StepmotorFahrwerk.STATE_ACC:
                if not self.accelerating:
                    self.accelerating = True
                    delay = self.accelerate(delay, self.steps_acc_stop)
                    if delay < StepmotorFahrwerk.delay_drive:
                        self.set_state(StepmotorFahrwerk.STATE_DRIVE)
                        self.accelerating = False
            else:
                self.stop(delay, self.steps_acc_stop)
                self.cleanup()

    def cleanup(self):
        self.distance = 0
        self.steps = 0
        self.steps_acc = 0
        self.steps_drive = 0
        self.steps_stop = 0
        self.steps_acc_stop = 0
