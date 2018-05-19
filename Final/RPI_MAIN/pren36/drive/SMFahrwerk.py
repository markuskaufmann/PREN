import math
from time import sleep
import RPi.GPIO as GPIO
import numpy as np

from pren36.lookup.Locator import Locator
from pren36.drive.AccelerationMode import AccelerationMode


class SMFahrwerk:
    DIR = 26  # Direction GPIO Pin GREEN
    STEP = 13  # Step GPIO Pin BLUE
    CW = 1  # Clockwise Rotation UP
    CCW = 0  # Counterclockwise Rotation DOWN
    RPM = 105
    RPS = RPM / 60
    SPR = 200
    STEP_MOD = 2  # 1/2 Step
    DELAY_MOD = 8
    SPS = RPS * (SPR * STEP_MOD)
    DIA_MOTOR = 5  # [mm]
    DIA = 82  # [mm]
    DIA_MOD = DIA / DIA_MOTOR
    PER = DIA_MOTOR * np.pi  # [mm]
    DPS = (PER / SPR) * DIA_MOD

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
    delay = delay_drive * DELAY_MOD  # 0.0208 / 2
    current_state = STATE_STOP
    current_direction = CW
    current_acc = AccelerationMode.MODE_START[1]
    accelerating = False
    stopping = False
    stop_req = False

    def __init__(self, direction):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(SMFahrwerk.DIR, GPIO.OUT)
        GPIO.setup(SMFahrwerk.STEP, GPIO.OUT)
        self.set_direction(direction)

    def set_state(self, state):
        self.current_state = state

    def set_acc_mode(self, mode):
        self.current_acc = mode

    def set_direction(self, direction):
        self.current_direction = direction
        self.set_state(SMFahrwerk.STATE_STOP)
        GPIO.output(SMFahrwerk.DIR, self.current_direction)

    def calc_acc(self, delay, steps):
        self.steps_acc = 0
        while delay > self.delay_drive and steps != 0:
            delay /= self.current_acc
            steps -= 1
            self.steps_acc += 1
        return delay, steps

    def calc_stop(self, delay, steps):
        self.steps_stop = 0
        while delay < self.delay and steps != 0:
            delay *= self.current_acc
            steps -= 1
            self.steps_stop += 1
        return steps

    def calc_steps(self, distance_mm):
        print("distance: %d [mm]" % distance_mm)
        if distance_mm == -1:
            self.distance = -1
            self.steps = -1
        else:
            self.distance = Locator.real_distance_mm(distance_mm)
            print("real distance: %f [mm]" % self.distance)
            revs = (self.distance / SMFahrwerk.PER) / SMFahrwerk.DIA_MOD
            print("revs: %f" % revs)
            self.steps = int(math.ceil(revs * SMFahrwerk.SPR * SMFahrwerk.STEP_MOD))
            print("steps calc: %d" % self.steps)
        d_acc, s_acc = self.calc_acc(self.delay, self.steps)
        s_stop = self.calc_stop(d_acc, self.steps)
        self.steps_acc_stop = self.steps_acc
        if self.steps != -1 and self.steps < (self.steps_acc + self.steps_stop):
            self.steps_acc_stop = int(math.ceil(self.steps / 2))
        print("steps acc / stop: %d" % self.steps_acc_stop)
        if self.steps == -1:
            self.steps_drive = -1
        else:
            self.steps_drive = self.steps - self.steps_acc_stop * 2
            if self.steps_drive < 0:
                self.steps_drive = 0
            print("steps drive: %d" % self.steps_drive)

    def accelerate(self, delay, steps):
        print("accelerate")
        while delay > self.delay_drive and steps != 0 and not self.stop_req:
            GPIO.output(SMFahrwerk.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(SMFahrwerk.STEP, GPIO.LOW)
            sleep(delay)
            delay /= self.current_acc
            steps -= 1
            Locator.update_loc_fahrwerk(SMFahrwerk.DPS)
        return delay

    def stop(self, delay, steps):
        if self.stopping:
            print("stop")
            while delay < self.delay and steps != 0:
                GPIO.output(SMFahrwerk.STEP, GPIO.HIGH)
                sleep(delay)
                GPIO.output(SMFahrwerk.STEP, GPIO.LOW)
                sleep(delay)
                delay *= self.current_acc
                steps -= 1
                Locator.update_loc_fahrwerk(SMFahrwerk.DPS)
            self.stopping = False
        return delay

    def drive(self, delay, step_count):
        print("drive")
        steps = 0
        while not self.stop_req and (steps < step_count or step_count == -1):
            GPIO.output(SMFahrwerk.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(SMFahrwerk.STEP, GPIO.LOW)
            sleep(delay)
            steps += 1
            Locator.update_loc_fahrwerk(SMFahrwerk.DPS)

    def move_distance(self, distance_mm, acc_mode):
        self.calc_steps(distance_mm)
        self.set_acc_mode(acc_mode[1])
        self.set_state(SMFahrwerk.STATE_ACC)

    def move_continuous(self, acc_mode):
        self.calc_steps(-1)
        self.set_acc_mode(acc_mode[1])
        self.set_state(SMFahrwerk.STATE_ACC)

    def request_stop(self):
        self.stop_req = True

    def control(self):
        delay = SMFahrwerk.delay
        while True:
            if self.current_state == SMFahrwerk.STATE_DRIVE:
                self.drive(delay, self.steps_drive)
                print("set stop")
                self.set_state(SMFahrwerk.STATE_STOP)
            elif self.current_state == SMFahrwerk.STATE_ACC:
                if not self.accelerating:
                    self.accelerating = True
                    self.stopping = True
                    self.stop_req = False
                    delay = self.accelerate(delay, self.steps_acc_stop)
                    if self.stop_req:
                        self.set_state(SMFahrwerk.STATE_STOP)
                        continue
                    print("set drive")
                    self.set_state(SMFahrwerk.STATE_DRIVE)
                    self.accelerating = False
            else:
                self.stop(delay, self.steps_acc_stop)
                # self.cleanup()

    def cleanup(self):
        self.distance = 0
        self.steps = 0
        self.steps_acc = 0
        self.steps_drive = 0
        self.steps_stop = 0
        self.steps_acc_stop = 0