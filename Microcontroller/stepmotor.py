from time import sleep
import RPi.GPIO as GPIO

DIR = 20  # Direction GPIO Pin
STEP = 21  # Step GPIO Pin
CW = 1  # Clockwise Rotation
CCW = 0  # Counterclockwise Rotation
SPR = 48  # Steps per Revolution

GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)       #DIR Pin als Ausgang definieren
GPIO.setup(STEP, GPIO.OUT)      #STEP Pin als Ausgang definieren
GPIO.output(DIR, CW)            #Default Richtung "im Uhrzeigersinn"
# Einstellungen Mode 0|1|2
# Müssen auf Hardware geändert werden!
# 000 Fullstep
# 100 1/2 Step
# 010 1/4 Step
# 110 8 microstep/step
# 001 16 microstep/step
# 101 32 microstep/step
#
#Das Programm wurde auf 16 microstep/step ausgelegt. Deshalb muss M2 noch auf 5V geschlossen werden

step_count = SPR * 16   # Microstep /16
state = { 'stop': 0,    # Zustände des Fahrens
          'acc': 1,
          'drive': 2}

# Verkürzt das Delay bis es kleiner als 0.0005/16 ist -> 1kHz
def accelerate(delay):
    while(delay > (0.0005/16)):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        delay /= 2
    return delay
# Verkürzt das Delay bis es zum Start-wert und hält dann ganz an
def stop(delay):
    while(delay < (0.02/16)):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
        delay *= 2
    return delay
# Normale Fahrt auf höchster Geschwindigkeit
def drive(delay):
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
def control():
    delay = 0.02/16
    while (True):
        if state == 'drive':
            stop(delay)
            break
        elif state == 'acc':
            accelerate(delay)
            if (delay < (0.0005/16)):
                state = 'drive'
            break
        else:
            stop(delay)
            break
