import RPi.GPIO as GPIO
import time


class Servomotor:
    GPIO_SERVO = 12

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_SERVO, GPIO.OUT)
    p = GPIO.PWM(GPIO_SERVO, 50)

    # dc_1 = 9.5
    # dc_2 = 5.5
    dc_1 = 5.5
    dc_2 = 10.5
    dc_sleep = 2

    def initialize(self, dc):
        Servomotor.p.start(dc)
        time.sleep(1)
        # Servomotor.p.ChangeDutyCycle(0)

    def reset(self):
        Servomotor.p.ChangeDutyCycle(Servomotor.dc_1)
        time.sleep(1)
        # Servomotor.p.ChangeDutyCycle(0)

    def open(self):
        Servomotor.p.ChangeDutyCycle(Servomotor.dc_1)
        time.sleep(1)
        # Servomotor.p.ChangeDutyCycle(0)

    def close(self):
        Servomotor.p.ChangeDutyCycle(Servomotor.dc_2)
        time.sleep(1)
        # Servomotor.p.ChangeDutyCycle(0)

    def stop(self):
        # self.reset()
        Servomotor.p.stop()
        # GPIO.cleanup()
