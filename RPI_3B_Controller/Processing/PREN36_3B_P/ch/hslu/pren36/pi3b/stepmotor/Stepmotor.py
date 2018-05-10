from time import sleep
import RPi.GPIO as GPIO
import numpy as np


class StepMotor:
    DIR = 21  # Direction GPIO Pin GREEN
    STEP = 16  # Step GPIO Pin BLUE
    CW = 1  # Clockwise Rotation DOWN
    CCW = 0  # Counterclockwise Rotation UP
    SPR = 48  # Steps per Revolution
    STEP_MOD = 32  # 32 microstep/step
    DIA = 15
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
    delay = 0.0208 / 4096
    delay_drive = 0.0005 / 4096
    state = {'stop': 0,
             'acc': 1,
             'drive': 2}
    current_state = state['stop']
    current_direction = CW
    accelerating = False

    def __init__(self, direction):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(StepMotor.DIR, GPIO.OUT)
        GPIO.setup(StepMotor.STEP, GPIO.OUT)
        self.set_direction(direction)

    def set_direction(self, direction):
        self.current_direction = direction
        self.set_state(StepMotor.state['stop'])
        GPIO.output(StepMotor.DIR, self.current_direction)

    def set_state(self, state):
        self.current_state = state

    # Verkürzt das Delay bis es kleiner als 0.0005/16 ist -> 1kHz
    def accelerate(self, delay):
        while delay > StepMotor.delay_drive:
            GPIO.output(StepMotor.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(StepMotor.STEP, GPIO.LOW)
            sleep(delay)
            delay /= 1.1
            self.steps_acc += 1
        return delay

    # Verkürzt das Delay bis es zum Start-wert und hält dann ganz an
    def stop(self, delay):
        while delay < StepMotor.delay:
            GPIO.output(StepMotor.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(StepMotor.STEP, GPIO.LOW)
            sleep(delay)
            delay *= 1.1
            self.steps_stop += 1
        return delay

    # Normale Fahrt auf höchster Geschwindigkeit
    def drive(self, delay):
        for i in range(0, self.step_count):
            GPIO.output(StepMotor.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(StepMotor.STEP, GPIO.LOW)
            sleep(delay)
            self.steps += 1

    def control(self):
        delay = StepMotor.delay
        while True:
            if self.current_state == StepMotor.state['drive']:
                # self.stop(delay)
                while self.current_state is not StepMotor.state['stop']:
                    self.drive(delay)
            elif self.current_state == StepMotor.state['acc']:
                if not self.accelerating:
                    self.accelerating = True
                    delay = self.accelerate(delay)
                    if delay < StepMotor.delay_drive:
                        self.current_state = StepMotor.state['drive']
                        self.accelerating = False
            else:
                self.stop(delay)
