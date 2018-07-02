import RPi.GPIO as GPIO
import time


class UltraSoundSensor:
    GPIO_TRIGGER = 22
    GPIO_ECHO = 17

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)

    def distance(self):
        # setze Trigger auf HIGH
        GPIO.output(UltraSoundSensor.GPIO_TRIGGER, True)

        # setze Trigger nach 0.01ms aus LOW
        time.sleep(0.00001)
        GPIO.output(UltraSoundSensor.GPIO_TRIGGER, False)

        time_start = time.time()
        time_stop = time.time()

        # speichere Startzeit
        while GPIO.input(UltraSoundSensor.GPIO_ECHO) == 0:
            time_start = time.time()

        # speichere Ankunftszeit
        while GPIO.input(UltraSoundSensor.GPIO_ECHO) == 1:
            time_stop = time.time()

        # Zeit Differenz zwischen Start und Ankunft
        time_elapsed = time_stop - time_start
        # mit der Schallgeschwindigkeit (34300 cm/s) multiplizieren
        # und durch 2 teilen, da hin und zurueck
        distance = (time_elapsed * 34300) / 2
        return distance

    def stop(self):
        GPIO.cleanup()
