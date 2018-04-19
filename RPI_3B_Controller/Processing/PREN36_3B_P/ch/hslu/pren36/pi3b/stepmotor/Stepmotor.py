from time import sleep
import RPi.GPIO as GPIO


class StepMotor:
    DIR = 20  # Direction GPIO Pin GREEN
    STEP = 21  # Step GPIO Pin BLUE
    CW = 1  # Clockwise Rotation DOWN
    CCW = 0  # Counterclockwise Rotation UP
    SPR = 48  # Steps per Revolution

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)       # DIR Pin als Ausgang definieren
    GPIO.setup(STEP, GPIO.OUT)      # STEP Pin als Ausgang definieren
    GPIO.output(DIR, CCW)            # Default Richtung "im Uhrzeigersinn"

    # Einstellungen Mode 0|1|2
    # Müssen auf Hardware geändert werden!
    # 000 Fullstep
    # 100 1/2 Step
    # 010 1/4 Step
    # 110 8 microstep/step
    # 001 16 microstep/step
    # 101 32 microstep/step
    #
    # Das Programm wurde auf 16 microstep/step ausgelegt. Deshalb muss M2 noch auf 5V geschlossen werden

    step_count = SPR * 32   # Microstep /16
    delay = 0.0208 / 4096
    delay_drive = 0.0005 / 4096
    state = {'stop': 0,    # Zustände des Fahrens
             'acc': 1,
             'drive': 2}
    current_state = state['stop']

    def set_state(self, state):
        self.current_state = state

    # Verkürzt das Delay bis es kleiner als 0.0005/16 ist -> 1kHz
    def accelerate(self, delay):
        while delay > StepMotor.delay_drive:
            GPIO.output(StepMotor.STEP, GPIO.HIGH)
            sleep(self.delay)
            GPIO.output(StepMotor.STEP, GPIO.LOW)
            sleep(self.delay)
            delay /= 2
        return delay

    # Verkürzt das Delay bis es zum Start-wert und hält dann ganz an
    def stop(self, delay):
        while delay < StepMotor.delay:
            GPIO.output(StepMotor.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(StepMotor.STEP, GPIO.LOW)
            sleep(delay)
            delay *= 2
        return delay

    # Normale Fahrt auf höchster Geschwindigkeit
    def drive(self, delay):
        for x in range(self.step_count):
            GPIO.output(StepMotor.STEP, GPIO.HIGH)
            sleep(delay)
            GPIO.output(StepMotor.STEP, GPIO.LOW)
            sleep(delay)

    def control(self):
        delay = StepMotor.delay
        while True:
            if self.current_state == StepMotor.state['drive']:
                self.stop(delay)
            elif self.current_state == StepMotor.state['acc']:
                self.accelerate(delay)
                if delay < StepMotor.delay_drive:
                    self.current_state = StepMotor.state['drive']
                    while self.current_state is not StepMotor.state['stop']:
                        self.drive(delay)
            else:
                self.stop(delay)
