import RPi.GPIO as GPIO
import time


class Servomotor:
    servoPIN = 2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
    p = GPIO.PWM(servoPIN, 50)  # GPIO 17 als PWM mit 50Hz
    dc_1 = 4.5
    dc_2 = 8.5
    dc_sleep = 3

    def start(self):
        print("Start")
        p = Servomotor.p
        p.start(2.5)  # Initialisierung
        try:
            p.ChangeDutyCycle(7.5)
            while True:
                p.ChangeDutyCycle(Servomotor.dc_1)
                time.sleep(0.5)
                p.ChangeDutyCycle(0)
                time.sleep(Servomotor.dc_sleep)
                p.ChangeDutyCycle(Servomotor.dc_2)
                time.sleep(Servomotor.dc_sleep)
                # p.ChangeDutyCycle(Servomotor.dc_1)
                # time.sleep(0.5)
                # p.ChangeDutyCycle(Servomotor.dc_2)
                # time.sleep(0.5)
                # p.ChangeDutyCycle(Servomotor.dc_1)
                # time.sleep(0.5)
                # p.ChangeDutyCycle(Servomotor.dc_2)
                # time.sleep(0.5)
                # p.ChangeDutyCycle(Servomotor.dc_1)
                # time.sleep(0.5)
                # p.ChangeDutyCycle(Servomotor.dc_2)
                # time.sleep(0.5)
                p.ChangeDutyCycle(7.5)
        except KeyboardInterrupt:
            p.ChangeDutyCycle(7.5)
            p.stop()
            GPIO.cleanup()
