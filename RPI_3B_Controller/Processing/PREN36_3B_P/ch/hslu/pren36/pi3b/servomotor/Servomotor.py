import RPi.GPIO as GPIO
import time


class Servomotor:
    GPIO_SERVO = 2

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GPIO_SERVO, GPIO.OUT)
    p = GPIO.PWM(GPIO_SERVO, 50)  # GPIO 2 als PWM mit 50Hz

    dc_1 = 4.5
    dc_2 = 8.5
    dc_sleep = 2

    # def start(self):
    #     p = Servomotor.p
    #     p.start(2.5)  # Initialisierung
    #     try:
    #         p.ChangeDutyCycle(7.5)
    #         time.sleep(0.5)
    #         while True:
    #             p.ChangeDutyCycle(Servomotor.dc_1)
    #             time.sleep(0.1)
    #             p.ChangeDutyCycle(0)
    #             time.sleep(Servomotor.dc_sleep)
    #             p.ChangeDutyCycle(Servomotor.dc_2)
    #             time.sleep(Servomotor.dc_sleep)
    #             # p.ChangeDutyCycle(Servomotor.dc_1)
    #             # time.sleep(0.5)
    #             # p.ChangeDutyCycle(Servomotor.dc_2)
    #             # time.sleep(0.5)
    #             # p.ChangeDutyCycle(Servomotor.dc_1)
    #             # time.sleep(0.5)
    #             # p.ChangeDutyCycle(Servomotor.dc_2)
    #             # time.sleep(0.5)
    #             # p.ChangeDutyCycle(Servomotor.dc_1)
    #             # time.sleep(0.5)
    #             # p.ChangeDutyCycle(Servomotor.dc_2)
    #             # time.sleep(0.5)
    #             p.ChangeDutyCycle(7.5)
    #     except KeyboardInterrupt:
    #         p.ChangeDutyCycle(7.5)
    #         p.stop()
    #         GPIO.cleanup()

    def initialize(self):
        Servomotor.p.start(2.5)

    def reset(self):
        Servomotor.p.ChangeDutyCycle(7.5)
        time.sleep(0.1)
        Servomotor.p.ChangeDutyCycle(0)

    def open(self):
        Servomotor.p.ChangeDutyCycle(Servomotor.dc_1)
        time.sleep(0.1)
        Servomotor.p.ChangeDutyCycle(0)

    def close(self):
        Servomotor.p.ChangeDutyCycle(Servomotor.dc_2)
        time.sleep(0.1)
        Servomotor.p.ChangeDutyCycle(0)

    def stop(self):
        self.reset()
        Servomotor.p.stop()
        GPIO.cleanup()
