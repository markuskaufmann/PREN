from time import sleep
import RPi.GPIO as GPIO


class DemoPin:
    delay = 0.0005

    def run(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(13, GPIO.OUT)
        while True:
            GPIO.output(13, GPIO.HIGH)
            sleep(DemoPin.delay)
            GPIO.output(13, GPIO.LOW)
            sleep(DemoPin.delay)


if __name__ == '__main__':
    pin = DemoPin()
    pin.run()
