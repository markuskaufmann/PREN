from time import sleep
import RPi.GPIO as GPIO
import numpy as np


class StepmotorFahrwerk:
    DIR = 13  # Direction GPIO Pin GREEN
    STEP = 26  # Step GPIO Pin BLUE
    CW = 1  # Clockwise Rotation
    CCW = 0  # Counterclockwise Rotation
    SPR = 200  # Steps per Revolution
    RPM = 105  # Revolutions per minute
    STEP_MOD = 2  # 1/2 Step
    DIA = 85
    PER = DIA * np.pi

    # Einstellungen Mode 0|1|2
    # Müssen auf Hardware geändert werden!
    # 000 Fullstep
    # 100 1/2 Step
    # 010 1/4 Step
    # 110 8 microstep/step
    # 001 16 microstep/step
    # 101 32 microstep/step

    step_count = SPR * STEP_MOD
    steps = 0
    steps_acc = 0
    steps_stop = 0
    delay = 1 / 100  # 0.0208 / 2
    delay_drive = 1 / 600  # 0.0005 / 4096
    state = {'stop': 0,
             'acc': 1,
             'drive': 2}
    current_state = state['stop']
    current_direction = CW
    accelerating = False

    def __init__(self, direction):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(StepmotorFahrwerk.DIR, GPIO.OUT)
        GPIO.setup(StepmotorFahrwerk.STEP, GPIO.OUT)
        self.set_direction(direction)

    def set_state(self, state):
        self.current_state = state

    def set_direction(self, direction):
        self.current_direction = direction
        self.set_state(StepmotorFahrwerk.state['stop'])
        GPIO.output(StepmotorFahrwerk.DIR, self.current_direction)

    # Verkürzt das Delay bis es kleiner als 0.0005/16 ist -> 1kHz
    def accelerate(self, delay):
        while delay > StepmotorFahrwerk.delay_drive:
            GPIO.output(StepmotorFahrwerk.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(StepmotorFahrwerk.STEP, GPIO.LOW)
            sleep(delay)
            delay /= 1.01
            self.steps_acc += 1
        return delay

    # Verkürzt das Delay bis es zum Start-wert und hält dann ganz an
    def stop(self, delay):
        while delay < StepmotorFahrwerk.delay:
            GPIO.output(StepmotorFahrwerk.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(StepmotorFahrwerk.STEP, GPIO.LOW)
            sleep(delay)
            delay *= 1.01
            self.steps_stop += 1
        return delay

    # Normale Fahrt auf höchster Geschwindigkeit
    def drive(self, delay):
        for step in range(0, self.step_count):
            GPIO.output(StepmotorFahrwerk.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(StepmotorFahrwerk.STEP, GPIO.LOW)
            sleep(delay)
            self.steps += 1

    def control(self):
        delay = StepmotorFahrwerk.delay
        while True:
            if self.current_state == StepmotorFahrwerk.state['drive']:
                # self.stop(delay)
                while self.current_state is not StepmotorFahrwerk.state['stop']:
                    self.drive(delay)
            elif self.current_state == StepmotorFahrwerk.state['acc']:
                if not self.accelerating:
                    self.accelerating = True
                    delay = self.accelerate(delay)
                    if delay < StepmotorFahrwerk.delay_drive:
                        self.current_state = StepmotorFahrwerk.state['drive']
                        self.accelerating = False
            else:
                self.stop(delay)
